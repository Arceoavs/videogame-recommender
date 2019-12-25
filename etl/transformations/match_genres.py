import py_stringsimjoin as ssj
import py_stringmatching as sm
import pandas as pd
from nltk.stem import PorterStemmer

from utilities import engine

with engine.connect() as connection:
  metacritic_genres = pd.read_sql_query(
    ''' 
    SELECT
      unnest(string_to_array(genres, ';')) as name 
    FROM metacritic.stage_games
    GROUP BY 1;
    ''',
    connection
  )

  # create key attribute
  metacritic_genres['id'] = range(0, len(metacritic_genres))

  igdb_genres = pd.read_sql_query(
    ''' 
    SELECT 
      id,
      TRIM(regexp_replace(name, '\(.*\)', '')) as name -- removes abbreviations in paranthesis
    FROM igdb.stage_genres;
    ''',
    connection
  )

  ### Matching

  porter = PorterStemmer()
  metacritic_genres['stem'] = metacritic_genres.name.apply(lambda s: porter.stem(s))
  igdb_genres['stem'] = igdb_genres.name.apply(lambda s: porter.stem(s))


  matching_pairs = ssj.edit_distance_join(
    metacritic_genres, igdb_genres, 
    'id', 'id', 
    'stem', 'stem', 
    0, 
    l_out_attrs=['stem', 'name'], r_out_attrs=['stem', 'name'],
    l_out_prefix='metacritic_', r_out_prefix='igdb_'
  )

  print(matching_pairs.head(20))
  matching_pairs.to_sql('genres', engine, schema='matching', if_exists='replace', index=False)

  ### Joining

  metacritic_merged = matching_pairs.merge(
    metacritic_genres, left_on='metacritic_name', right_on='name', how='outer'
  )
  metacritic_merged['metacritic_name'] = metacritic_merged['name']

  igdb_merged = matching_pairs.merge(
    igdb_genres, left_on='igdb_id', right_on='id', how='outer'
  )
  igdb_merged['igdb_id'] = igdb_merged['id']
  igdb_merged = igdb_merged[igdb_merged.metacritic_name.isnull()]

  merged = pd.concat([metacritic_merged, igdb_merged], sort=False, ignore_index=True)
  merged = merged[['name', 'igdb_id', 'metacritic_name']]
  merged.to_sql('genres', engine, schema='lookup', if_exists='replace', index_label='id')

  ### CREATE FACT TABLE

  connection.execute(
    """
    DROP TABLE IF EXISTS genres;
    CREATE TABLE genres (
      id int NOT NULL PRIMARY KEY,
      name varchar(255)
    );
    INSERT INTO genres
    SELECT id, name
    FROM lookup.genres;
    """
  )

  connection.close()
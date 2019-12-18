import py_stringsimjoin as ssj
import py_stringmatching as sm
import pandas as pd

from utilities import engine
from game_tokenizer import GameTokenizer

with engine.connect() as connection:
  igdb_games = pd.read_sql_query(
    ''' 
    SELECT * FROM (
      SELECT 
        g.id,
        trim(unnest(array_append(a.alternative_names, g.name))) as title,
        EXTRACT('YEAR' FROM g.first_release_date) as year,
        array_to_string(g.platforms, ', ') as platforms
      FROM igdb.stage_games g
      LEFT JOIN (
        SELECT game as game_id, array_agg(name) as alternative_names FROM igdb.stage_alternative_names GROUP BY 1
      ) a ON g.id = a.game_id
    ) g WHERE platforms IS NOT null OR year IS NOT null;
    ''',
    connection
  )

  giantbomb_games = pd.read_sql_query(
    ''' 
    SELECT * FROM (
      SELECT 
        id, 
        trim(unnest(array_append(string_to_array(aliases, ','), g.game_name))) as title, 
        year,
        g.platform as platforms 
      FROM giantbomb.stage_games g
      LEFT JOIN (SELECT game_id, EXTRACT('YEAR' FROM min(release_date)) as year from giantbomb.stage_releases GROUP BY 1) r
      ON g.id = r.game_id
    ) g WHERE title IS NOT null AND title <> '' AND (platforms IS NOT null OR year IS NOT null);
    ''',
    connection
  )

  igdb_games['key'] = range(0, len(igdb_games))
  giantbomb_games['key'] = range(0, len(giantbomb_games))

  print(ssj.profile_table_for_join(igdb_games))
  print(ssj.profile_table_for_join(giantbomb_games))

  # porter = PorterStemmer()
  # metacritic_genres['stem'] = metacritic_genres.name.apply(lambda s: porter.stem(s))
  # print(metacritic_genres.head(10))

  # igdb_genres['stem'] = igdb_genres.name.apply(lambda s: porter.stem(s))
  # print(igdb_genres.head(21))
  # # ws = sm.WhitespaceTokenizer(return_set=True)

  gt = GameTokenizer()

  mc = ssj.jaccard_join(
    igdb_games, giantbomb_games, 
    'key', 'key', 
    'title', 'title', 
    gt, 0.5, 
    l_out_attrs=['id', 'title', 'year', 'platforms'], r_out_attrs=['id', 'title', 'year', 'platforms'],
    l_out_prefix='igdb_', r_out_prefix='giantbomb_'
  )

  print(mc)

  print(f'Found ${len(mc)} potential matching candidates')
  #mc.to_sql('game_candidates_0_5_gt', engine, schema='matching', if_exists='replace', index_label='key')


  mc = mc[mc.igdb_year == mc.giantbomb_year]
  print(f'After year cleaning ${len(mc)} potential matching candidates')


  first_igdb = mc.groupby(mc.igdb_id) #.sort_values(_sim_score, ascending=False).first()
  print(first_igdb.head(10))

  print(mc.head(20))
  #mc.to_sql('filtered_game_candidates', engine, schema='matching', if_exists='replace', index_label='key')

  connection.close()



  # # print("######")
  # # output_pairs2 = ssj.edit_distance_join(
  # #   metacritic_genres, igdb_genres, 
  # #   'id', 'id', 
  # #   'name', 'name', 
  # #   3, 
  # #   l_out_attrs=['name'], r_out_attrs=['name']
  # # )
  # # print(output_pairs2)
  # print("######")
  # matching_pairs = ssj.edit_distance_join(
  #   metacritic_genres, igdb_genres, 
  #   'id', 'id', 
  #   'stem', 'stem', 
  #   0, 
  #   l_out_attrs=['stem', 'name'], r_out_attrs=['stem', 'name'],
  #   l_out_prefix='metacritic_', r_out_prefix='igdb_'
  # )
  # print(matching_pairs)

  # # merged = pd.merge(
  # #   metacritic_genres, matching_pairs, left_on='name', right_on='metacritic_name', how='left'
  # #   ).merge(
  # #     igdb_genres, left_on='igdb_id', right_on='id', how='outer'
  # #   )
  # # print(merged.head(200))

  # # merged = matching_pairs.merge(
  # #     metacritic_genres, left_on='metacritic_name', right_on='name', how='outer'
  # #   ).merge(
  # #     igdb_genres, left_on='igdb_id', right_on='id', how='outer'
  # #   )

  # metacritic_merged = matching_pairs.merge(
  #   metacritic_genres, left_on='metacritic_name', right_on='name', how='outer'
  # )
  # metacritic_merged['metacritic_name'] = metacritic_merged['name']
    
  # igdb_merged = matching_pairs.merge(
  #   igdb_genres, left_on='igdb_id', right_on='id', how='outer'
  # )
  # igdb_merged['igdb_id'] = igdb_merged['id']
  # igdb_merged = igdb_merged[igdb_merged.metacritic_name.isnull()]

  # print(igdb_merged.head(21))

  # merged = pd.concat([metacritic_merged, igdb_merged], sort=False, ignore_index=True)

  # merged.to_sql('test_genres', engine, if_exists='replace', index=False)


  # merged = merged[['name', 'igdb_id', 'metacritic_name']]

  # print(merged.tail(20))

  # merged.to_sql('dim_genres', engine, schema='dimension', if_exists='replace', index_label='id')
  # connection.close()
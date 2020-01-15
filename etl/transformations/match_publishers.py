import py_stringsimjoin as ssj
import py_stringmatching as sm
import pandas as pd
import sqlalchemy
from pandas import DataFrame


from utilities import engine

with engine.connect() as connection:
    # giantBomb_publishers = pd.read_sql_query(
    #     '''
    #     SELECT description regexp_matches('published by\s+\K\S+ ') FROM giantbomb.stage_games;
    #     ''',
    #     connection
    # )

    igdb_publishers = pd.read_sql_query(
        ''' 
        SELECT max(id) AS id, name AS publisher
        FROM igdb.stage_companies
        WHERE name IS NOT NULL
        GROUP BY name;
        ''',
        connection
    )

    metacritic_publishers: DataFrame = pd.read_sql_query(
        ''' 
        SELECT max(id) AS id, publisher AS publisher
                FROM metacritic.stage_games
                WHERE publisher IS NOT NULL
        		GROUP BY publisher;
        		
        ''',
        connection
    )

    matching_publishers = ssj.edit_distance_join(
        igdb_publishers, metacritic_publishers,
        'id', 'id',
        'publisher', 'publisher',
        0,
        #TODO: Evaluate if treshold of 0 makes sense - this is equivalent to a normal join on the publisher names, it doesn't match any publishers with different names
        l_out_attrs=['id', 'publisher'], r_out_attrs=['id', 'publisher'],
        l_out_prefix='igdb_', r_out_prefix='metacritic_'
    )

    matching_publishers.to_sql('publishers', engine, schema='matching', if_exists='replace', index=False)

# renaming the columns to similar and dissimilar names in both dataframes

    # oriented on  match_platforms:
    metacritic_merged = matching_publishers.merge(
        metacritic_publishers, left_on='metacritic_id', right_on='id', how='right'
    )

    metacritic_merged['metacritic_id'] = metacritic_merged['id']

    print(metacritic_merged[['metacritic_id', 'publisher']])

    igdb_merged = matching_publishers.merge(
        igdb_publishers, left_on='igdb_id', right_on='id', how='right'
    )

    igdb_merged['igdb_id'] = igdb_merged['id']
    print(igdb_merged[['igdb_id','publisher']])
    igdb_merged = igdb_merged[igdb_merged.metacritic_id.isnull()]

    merged = pd.concat([metacritic_merged, igdb_merged], sort=False, ignore_index=True)
    merged = merged[['publisher', 'metacritic_id', 'igdb_id']]

    merged.to_sql('publishers', engine, schema='lookup', if_exists='replace', index_label='id', dtype={
        'id': sqlalchemy.types.INT,
        'publisher': sqlalchemy.types.VARCHAR,
        'metacritic_id': sqlalchemy.types.INT,
        'igdb_id': sqlalchemy.types.INT,
      })

    final_publishers=merged[['publisher']]

    #TODO: Create publisher schema with Flask
    final_publishers.to_sql('publishers', engine, if_exists='replace', index_label='id', dtype={
        'id': sqlalchemy.types.INT,
        'publisher': sqlalchemy.types.VARCHAR
    })


    #print(metacritic_merged)

    # integrated_publishers = pd.concat([metacritic_publishers, igdb_publishers], join="outer",
    #                                   ignore_index=True, keys=None, levels=None, names=None, verify_integrity=False,
    #                                   sort=True, copy=True)
    #
    # integrated_publishers.to_sql('integrated_publishers', engine, schema='public', if_exists='replace', index=False)

    # connection.execute(
    #     """
    #     ALTER TABLE integrated_publishers ADD PRIMARY KEY (ID);
    #     """
    #     )


    connection.close()


    # print(tabulate(igdb_publishers.head(10)))
    # print(tabulate(matching_publishers.head(10)))
    # print(matching_publishers)
    # print("integrated publichers")
    # print(tabulate(integrated_publishers.head(10)))


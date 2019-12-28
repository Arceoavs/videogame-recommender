import py_stringsimjoin as ssj
import py_stringmatching as sm
import pandas as pd
from pandas import DataFrame
from tabulate import tabulate

from utilities import engine

with engine.connect() as connection:
    # TODO: refactor and test regular expression to extract publishers from natural language from datasource giantbomb

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
        l_out_attrs=['id', 'publisher'], r_out_attrs=['id', 'publisher'],
        l_out_prefix='metacritic_', r_out_prefix='igdb_'
    )

    matching_publishers.to_sql('publishers', engine, schema='matching', if_exists='replace', index=False)

# renaming the columns to similar and dissimilar names in both dataframes

    integrated_publishers = pd.concat([metacritic_publishers, igdb_publishers], join="outer",
                                      ignore_index=True, keys=None, levels=None, names=None, verify_integrity=False,
                                      sort=True, copy=True)

    integrated_publishers.to_sql('integrated_publishers', engine, schema='public', if_exists='replace', index=False)

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


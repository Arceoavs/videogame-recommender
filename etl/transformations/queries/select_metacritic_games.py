import pandas as pd

def select_metacritic_games(connection):
  return pd.read_sql_query(
    ''' 
    SELECT Array_agg(id)                   AS ids,
           title,
           Min(year)                       AS "year",
           String_agg(DISTINCT NAME, ', ') AS platforms
    FROM   (SELECT m.id,
                   m.title,
                   m.year,
                   p.NAME
            FROM   metacritic.stage_games m
                   LEFT JOIN lookup.platforms p
                          ON p.metacritic_name = m.platform) t
    GROUP  BY title; 
    ''',
    connection
  )
import pandas as pd

def select_metacritic_games(connection):
  return pd.read_sql_query(
    ''' 
    SELECT MIN(id) AS id,
           title,
           Min(year) AS "year",
           string_agg(DISTINCT NAME, ', ') AS platforms
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
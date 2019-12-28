import pandas as pd

def select_metacritic_games(connection):
  return pd.read_sql_query(
    ''' 
    SELECT Array_agg(id)                AS ids,
           title,
           Min(year)                    AS "year",
           Array_agg(DISTINCT platform) AS platforms
    FROM   metacritic.stage_games
    GROUP  BY title; 
    ''',
    connection
  )
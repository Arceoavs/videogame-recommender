import pandas as pd

def select_metacritic_users(connection):
  return pd.read_sql_query(
    ''' 
    select distinct username "name" from metacritic.stage_user_comments;
    ''',
    connection
  )
import pandas as pd

def select_igdb_users(connection):
  return pd.read_sql_query(
    ''' 
    SELECT DISTINCT
                                        "user" id
                                FROM
                                        igdb.stage_ratings;
    ''',
    connection
  )
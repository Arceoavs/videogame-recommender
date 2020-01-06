import pandas as pd

def select_giantbomb_users(connection):
  return pd.read_sql_query(
    ''' 
    SELECT DISTINCT
                                        username      "name"
                                FROM
                                        giantbomb.stage_reviews;
    ''',
    connection
  )
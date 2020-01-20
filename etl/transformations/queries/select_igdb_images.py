import pandas as pd

def select_igdb_images(connection):
  return pd.read_sql_query(
    '''
    SELECT l.id,
           i.image_link as image_url
    FROM   igdb.stage_images i
           INNER JOIN lookup.games l
                   ON i.igdb_id = l.igdb_id 
        ''',
    connection
  )
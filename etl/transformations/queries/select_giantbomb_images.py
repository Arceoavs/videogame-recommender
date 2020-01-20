import pandas as pd

def select_giantbomb_images(connection):
  return pd.read_sql_query(
    '''
    SELECT l.id,
           i.image_link as image_url
    FROM   giantbomb.stage_images i
           INNER JOIN lookup.games l
                   ON i.giantbomb_id = l.giantbomb_id 
        ''',
    connection
  )
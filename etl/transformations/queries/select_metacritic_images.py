import pandas as pd

def select_metacritic_images(connection):
  return pd.read_sql_query(
    '''
    SELECT l.id,
           i.image_link as image_url
    FROM   metacritic.stage_images i
           INNER JOIN lookup.games l
                   ON i.metacritic_id = l.giantbomb_id 
        ''',
    connection
  )
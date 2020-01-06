import pandas as pd

def select_giantbomb_ratings(connection):
  return pd.read_sql_query(
    ''' 
    SELECT u.giantbomb_name       AS giantbomb_user_name,
           u.id                   AS user_id,
           g.giantbomb_id         AS giantbomb_game_id,
           g.id                   AS game_id,
           r.score * 2 :: INTEGER rating
    FROM   giantbomb.stage_reviews r
           inner join lookup.users u
                   ON r.username = u.giantbomb_name
           inner join lookup.games g
                   ON r.game_id = g.giantbomb_id;
    ''',
    connection
  )
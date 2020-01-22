import pandas as pd

def select_giantbomb_ratings(connection):
  return pd.read_sql_query(
    ''' 
    SELECT DISTINCT u.id                   AS user_id,
                    g.id                   AS game_id,
                    r.score * 2 :: INTEGER AS "value"
    FROM   giantbomb.stage_user_reviews r
           inner join (SELECT id,
                              Split_part(username, '@giantbomb.user', 1) AS username
                       FROM   users
                       WHERE  username LIKE '%%giantbomb%%') u
                   ON r.username = u.username
           inner join lookup.games g
                   ON r.game_id = g.giantbomb_id 
    ''',
    connection
  )
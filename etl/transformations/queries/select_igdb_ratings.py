import pandas as pd

def select_igdb_ratings(connection):
  return pd.read_sql_query(
    ''' 
    SELECT u.id                       AS user_id,
           g.id                       AS game_id,
           Round(r.rating) :: INTEGER AS "value"
    FROM   igdb.stage_ratings r
           inner join (SELECT id,
                              Split_part(username, '@igdb.user', 1) AS username
                       FROM   users
                       WHERE  username LIKE '%%igdb%%') u
                   ON Cast(r.USER AS VARCHAR) = u.username
           inner join lookup.games g
                   ON r.game = g.igdb_id; 
    ''',
    connection
  )
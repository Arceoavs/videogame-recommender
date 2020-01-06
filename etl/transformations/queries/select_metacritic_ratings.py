import pandas as pd

def select_metacritic_ratings(connection):
  return pd.read_sql_query(
    ''' 
    SELECT u.metacritic_name AS metacritic_user_name,
           u.id              AS user_id,
           g.metacritic_id   AS metacritic_game_id,
           g.id              AS game_id,
           r.userscore       rating
    FROM   metacritic.stage_user_comments r
           INNER JOIN lookup.users u
                   ON r.username = u.metacritic_name
           INNER JOIN metacritic.stage_games s_g
                   ON ( r.title = s_g.title
                        AND r.platform = s_g.platform )
           INNER JOIN lookup.games g
                   ON s_g.id = g.metacritic_id ;						
    ''',
    connection
  )
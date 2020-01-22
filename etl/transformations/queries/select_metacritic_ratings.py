import pandas as pd

def select_metacritic_ratings(connection):
  return pd.read_sql_query(
    '''
    SELECT DISTINCT u.id        AS user_id,
                    g.id        AS game_id,
                    r.userscore AS "value"
    FROM   metacritic.stage_user_comments r
           INNER JOIN (SELECT id,
                              Split_part(username, '@metacritic.user', 1) AS
                              username
                       FROM   users
                       WHERE  username LIKE '%%metacritic%%') u
                   ON r.username = u.username
           INNER JOIN (SELECT Min(id) AS id,
                              title
                       FROM   metacritic.stage_games m
                       GROUP  BY title) m_g
                   ON r.title = m_g.title
           INNER JOIN lookup.games g
                   ON m_g.id = g.metacritic_id 
    ''',
    connection
  )
import pandas as pd

def select_igdb_ratings(connection):
  return pd.read_sql_query(
    ''' 
    SELECT
        u.id AS user_id,
        g.id AS game_id,
        ROUND(r.rating)::integer "value"
    FROM
        igdb.stage_ratings r
    INNER JOIN
        (SELECT id, SPLIT_PART(username, '@igdb.user', 1) as username FROM users) u
    ON
        CAST(r.user AS varchar)=u.username
    INNER JOIN
        lookup.games g
    ON
        r.game=g.igdb_id;
    ''',
    connection
  )
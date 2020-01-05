import pandas as pd

def select_igdb_ratings(connection):
  return pd.read_sql_query(
    ''' 
    SELECT
                        u.igdb_id                     AS igdb_user_id,
						u.id							AS user_id,
                        g.igdb_id                     AS igdb_game_id,
						g.id							AS game_id,
                        ROUND(r.rating)::integer    rating
                FROM
                        igdb.stage_ratings r
                INNER JOIN
                        lookup.users u
                ON
                        r.user=u.igdb_id
                INNER JOIN
                        lookup.games g
                ON
                        r.game=g.igdb_id;
    ''',
    connection
  )
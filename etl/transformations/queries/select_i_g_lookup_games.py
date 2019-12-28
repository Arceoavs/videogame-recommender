import pandas as pd

def select_i_g_lookup_games(connection):
  return pd.read_sql_query(
    ''' 
    SELECT id,
           title,
           String_agg(DISTINCT platform, ', ') AS platforms,
           Min(year)                           AS year
    FROM  (SELECT id,
                  title,
                  Unnest(String_to_array(String_agg(platforms, ', '), ', ')) AS
                  platform,
                  Min(year)                                                  AS year
           FROM   (SELECT g.id,
                          c.igdb_title     AS title,
                          c.igdb_platforms AS platforms,
                          c.igdb_year      AS year
                   FROM   lookup.games g
                          LEFT JOIN matching.filtered_game_candidates c
                                 ON g.igdb_id = c.igdb_id
                                    AND g.giantbomb_id = c.giantbomb_id
                   UNION
                   SELECT g.id,
                          c.giantbomb_title,
                          c.giantbomb_platforms,
                          c.giantbomb_year
                   FROM   lookup.games g
                          LEFT JOIN matching.filtered_game_candidates c
                                 ON g.igdb_id = c.igdb_id
                                    AND g.giantbomb_id = c.giantbomb_id) t
           GROUP  BY id,
                     title
           ORDER  BY id) t2
    GROUP  BY id,
              title 
    ''',
    connection
  )
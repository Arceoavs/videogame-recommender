import pandas as pd

def select_unmatched_metacritic_games(connection):
  return pd.read_sql_query(
    ''' 
    SELECT id as metacritic_id
    FROM (
      SELECT 
        MIN(id) AS id,
        title,
        Min(year) AS "year",
        string_agg(DISTINCT NAME, ', ') AS platforms
      FROM (
        SELECT
          m.id,
          m.title,
          m.year,
          p.NAME
        FROM metacritic.stage_games m
        LEFT JOIN lookup.platforms p
        ON p.metacritic_name = m.platform) t
      GROUP  BY title
    ) m
    LEFT JOIN (
      SELECT
        m.metacritic_id
      FROM
        igdb.stage_games i
      FULL OUTER JOIN (
        SELECT igdb_id, giantbomb_id FROM matching.games_ig GROUP BY 1, 2
      ) g ON i.id = g.igdb_id
      FULL OUTER JOIN (
        SELECT igdb_id, metacritic_id FROM matching.games_im GROUP BY 1, 2
      ) m ON i.id = m.igdb_id
      GROUP BY 1
    ) igm ON igm.metacritic_id = m.id
    WHERE metacritic_id IS null;
    ''',
    connection
  )
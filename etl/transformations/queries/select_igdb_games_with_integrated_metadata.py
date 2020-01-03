import pandas as pd

def select_igdb_games_with_integrated_metadata(connection):
  return pd.read_sql_query(
    ''' 
    SELECT
      g.id, 
      g.title,
      g.summary as description,
      g.year, 
      string_agg(distinct CAST(g.platform_id AS varchar), ', ') AS platform_ids,
      string_agg(distinct CAST(gn.id AS varchar), ', ') AS genre_ids
    FROM (
      SELECT
        g.id,
        g.title,
        g.summary,
        g.year,
        p.id as platform_id,
        unnest(g.genres) as genre
      FROM (
        SELECT 
	        g.id,
	        g.name as title,
	        g.summary,
	        EXTRACT('YEAR' FROM g.first_release_date) AS year,
	        g.genres,
	        unnest(g.platforms) AS platform
        FROM igdb.stage_games g
      ) g
      FULL OUTER JOIN lookup.platforms p ON p.igdb_id = g.platform
    ) g
    FULL OUTER JOIN lookup.genres gn ON gn.igdb_id = g.genre
    GROUP BY 1,2,3,4;
    ''',
    connection
  )
import pandas as pd

def select_giantbomb_games_with_integrated_metadata(connection):
  return pd.read_sql_query(
    ''' 
    SELECT
      games.id,
      games.game_name as title,
      games.description,
      releases.year,
      STRING_AGG(DISTINCT CAST(platform_id AS varchar), ', ') as platform_ids
    FROM giantbomb.stage_games games
    -- game-release-association
    LEFT JOIN (
      (SELECT game_id, EXTRACT('YEAR' FROM min(release_date)) as year from giantbomb.stage_releases GROUP BY 1)
    ) releases ON releases.game_id = games.id
    -- game-platforms-association
    LEFT JOIN (
      SELECT g.id as game_id, l.id as platform_id FROM 
      ( SELECT id, trim(unnest(string_to_array(platform, ','))) as platform_name FROM giantbomb.stage_games) g
      LEFT JOIN giantbomb.stage_platforms op ON op.name = g.platform_name
      LEFT JOIN lookup.platforms l ON l.giantbomb_id = op.id
    ) platforms ON platforms.game_id = games.id
    GROUP BY 1,2,3,4;
    ''',
    connection
  )
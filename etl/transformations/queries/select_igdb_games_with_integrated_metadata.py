import pandas as pd

def select_igdb_games_with_integrated_metadata(connection):
  return pd.read_sql_query(
    ''' 
    SELECT
      game.id,
      game.name AS title,
      game.summary AS description,
      EXTRACT('YEAR' FROM game.first_release_date) AS year,
      STRING_AGG(DISTINCT CAST(platforms.platform_id AS varchar), ', ') AS platform_ids,
      STRING_AGG(DISTINCT CAST(genres.genre_id AS varchar), ', ') AS genre_ids
    FROM igdb.stage_games game
    -- game-platform-associations
    LEFT JOIN (
      SELECT g.id AS game_id, l.id AS platform_id FROM 
      (SELECT id, unnest(platforms) AS platform_id FROM igdb.stage_games) g
      LEFT JOIN lookup.platforms l ON l.igdb_id = g.platform_id
    ) platforms ON platforms.game_id = game.id
    -- game-genre-associations
    LEFT JOIN (
      SELECT g.id AS game_id, l.id AS genre_id FROM 
      (SELECT id, unnest(genres) AS genre_id FROM igdb.stage_games) g
      LEFT JOIN lookup.genres l ON l.igdb_id = g.genre_id
    ) genres ON genres.game_id = game.id
    GROUP BY 1,2,3,4;
    ''',
    connection
  )

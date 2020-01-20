import pandas as pd


def select_giantbomb_games(connection):
    return pd.read_sql_query(
        ''' 
        SELECT * FROM (
          SELECT
            game.id,
            trim(unnest(array_append(string_to_array(game.aliases, ','), game.game_name))) as title,
            release.year,
            platform.platforms
          FROM giantbomb.stage_games game
          -- join releases
          LEFT JOIN (SELECT game_id, EXTRACT('YEAR' FROM min(release_date)) as year from giantbomb.stage_releases GROUP BY 1) release
          ON game.id = release.game_id
          -- join platforms
          LEFT JOIN (
            SELECT game.id as game_id, string_agg(DISTINCT l_platform.name, ', ') as platforms FROM (
              SELECT
                id,
                trim(unnest(string_to_array(game.platform, ','))) as platform
              FROM giantbomb.stage_games game
            ) game
            LEFT JOIN giantbomb.stage_platforms gb_platform ON gb_platform.name = game.platform
            LEFT JOIN lookup.platforms l_platform ON l_platform.giantbomb_id = gb_platform.id
            GROUP BY 1
          ) platform
          ON game.id = platform.game_id
        ) game
        WHERE game.title IS NOT null AND game.title <> '';
        ''',
        connection
    )

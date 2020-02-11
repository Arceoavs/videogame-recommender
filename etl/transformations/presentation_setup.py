from utilities import engine

'''
Modifications to the database to make it more performant for the final presentation. 
Should not be executed in productive environment as it reduces the size of the database (mostly games without ratings).
'''
with engine.connect() as connection:
    connection.execute(
    """
    DELETE FROM game_genres WHERE game_id IN (
      SELECT DISTINCT game.id
      FROM games game
      LEFT JOIN ratings rating
      ON game.id = rating.game_id
      WHERE rating.id IS NULL
    );

    DELETE FROM game_platforms WHERE game_id IN (
      SELECT DISTINCT game.id
      FROM games game
      LEFT JOIN ratings rating
      ON game.id = rating.game_id
      WHERE rating.id IS NULL
    );

    CREATE TEMP TABLE genres_tmp AS SELECT * FROM game_genres;
    CREATE TEMP TABLE platforms_tmp AS SELECT * FROM game_platforms;
    CREATE TEMP TABLE ratings_tmp AS SELECT * FROM ratings;
    CREATE TEMP TABLE games_tmp AS (
      SELECT g.*
      FROM games g
      LEFT JOIN ratings r ON r.game_id = g.id
      WHERE r.id IS NOT NULL
      GROUP BY 1,2,3,4,5
    );

    TRUNCATE game_genres;
    TRUNCATE game_platforms;
    TRUNCATE ratings;
    DELETE FROM games;

    INSERT INTO games (SELECT * FROM games_tmp);
    INSERT INTO game_genres (SELECT * FROM genres_tmp);
    INSERT INTO game_platforms (SELECT * FROM platforms_tmp);
    INSERT INTO ratings (SELECT * FROM ratings_tmp);

    DROP TABLE IF EXISTS genres_tmp;
    DROP TABLE IF EXISTS platforms_tmp;
    DROP TABLE IF EXISTS games_tmp;
    DROP TABLE IF EXISTS ratings_tmp;
    """
    )

    connection.close()

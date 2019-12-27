from utilities import engine

with engine.connect() as connection:
  connection.execute("""
    DROP TABLE
        IF EXISTS core.ratings CASCADE
    """)
  connection.execute("""
    CREATE TABLE
        core.ratings AS
        (
                SELECT
                        u.id                     AS user_id,
                        g.id                     AS game_id,
                        ROUND(r.rating)::integer    rating
                FROM
                        igdb.stage_ratings r
                INNER JOIN
                        core.users u
                ON
                        r.user=u.igdb_id
                INNER JOIN
                        core.games g
                ON
                        r.game=g.igdb_id
                
                UNION
                
                SELECT
                        u.id               AS user_id,
                        g.id               AS game_id,
                        r.score*2::integer    rating
                FROM
                        giantbomb.stage_reviews r
                INNER JOIN
                        core.users u
                ON
                        r.username=u.giantbomb_name
                INNER JOIN
                        core.games g
                ON
                        r.game_id=g.giantbomb_id
        )
  """)
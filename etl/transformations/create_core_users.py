from utilities import engine

with engine.connect() as connection:
  connection.execute("""
    DROP TABLE
        IF EXISTS core.users CASCADE
    """)
  connection.execute("""
    CREATE TABLE
        core.users AS
        (
                SELECT
                        row_number() over(ORDER BY igdb_id) id,
                        *
                FROM
                        (
                                SELECT DISTINCT
                                        "user" igdb_id,
                                        NULL   giantbomb_name
                                FROM
                                        igdb.stage_ratings
                                
                                UNION
                                
                                SELECT DISTINCT
                                        NULL::integer igdb_id,
                                        username      giantbomb_name
                                FROM
                                        giantbomb.stage_reviews) t
        )
  """)
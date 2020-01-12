import pandas as pd
import sqlalchemy
from utilities import engine
from queries import (
  select_igdb_ratings,
select_giantbomb_ratings,
select_metacritic_ratings
)
with engine.connect() as connection:
    
    connection.execute('DELETE FROM ratings CASCADE')
    i_ratings = select_igdb_ratings.select_igdb_ratings(connection)
    i_ratings.to_sql('ratings', engine, if_exists='append', index=False)

    connection.close()
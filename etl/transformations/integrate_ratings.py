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
    i_ratings = select_igdb_ratings(connection)
    i_ratings.to_sql('ratings', engine, if_exists='append', index=False)
    print(f'[Integrate Ratings] {len(i_ratings)} IGDB ratings loaded into database')

    g_ratings = select_giantbomb_ratings(connection)
    g_ratings.to_sql('ratings', engine, if_exists='append', index=False)
    print(f'[Integrate Ratings] {len(g_ratings)} Giantbomb ratings loaded into database')

    m_ratings = select_metacritic_ratings(connection)
    m_ratings.to_sql('ratings', engine, if_exists='append', index=False)
    print(f'[Integrate Ratings] {len(m_ratings)} Metaritic ratings loaded into database')

    connection.close()
from utilities import engine

with engine.connect() as connection:
  connection.execute('DROP SCHEMA IF EXISTS igdb CASCADE')
  connection.execute('DROP SCHEMA IF EXISTS giantbomb CASCADE')
  connection.execute('DROP SCHEMA IF EXISTS metacritic CASCADE')
  connection.execute('DROP SCHEMA IF EXISTS matching CASCADE')
  connection.execute('DROP SCHEMA IF EXISTS lookup CASCADE')

  connection.close()

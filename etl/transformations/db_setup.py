from utilities import engine

with engine.connect() as connection:
  connection.execute("""CREATE SCHEMA IF NOT EXISTS igdb""")
  connection.execute("""CREATE SCHEMA IF NOT EXISTS giantbomb""")
  connection.execute("""CREATE SCHEMA IF NOT EXISTS metacritic""")
  connection.execute("""CREATE SCHEMA IF NOT EXISTS matching""")
  connection.execute("""CREATE SCHEMA IF NOT EXISTS lookup""")
  connection.execute("""CREATE SCHEMA IF NOT EXISTS core""")

  connection.close()

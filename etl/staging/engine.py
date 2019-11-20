import os
from sqlalchemy import create_engine

HOST = os.getenv('POSTGRES_HOST', 'localhost')
PORT = os.getenv('POSTGRES_PORT', '5432')
USER = os.getenv('POSTGRES_USER', 'videogamer')
PASSWORD = os.getenv('POSTGRES_PASSWORD', 'pwned-by-headshot-1337')
DB = os.getenv('POSTGRESS_DB', 'videogames')

engine = create_engine(f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}')
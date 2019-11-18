import os
from sqlalchemy import create_engine

HOST = os.getenv('HOST', 'localhost')
PORT = os.getenv('PORT', '5432')
DB_USER = os.getenv('DB_USER', 'videogamer')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'pwned-by-headshot-1337')
DB = os.getenv('DB', 'videogames')

engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{HOST}:{PORT}/{DB}')
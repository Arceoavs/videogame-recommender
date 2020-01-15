# this file structure follows http://flask.pocoo.org/docs/1.0/patterns/appfactories/
# initializing db in api.models.base instead of in api.__init__.py
# to prevent circular dependencies
from .base import db
from .DataModel import Game
from .DataModel import Genre
from .DataModel import Platform
from .RevokedToken import RevokedToken
from .User import User

__all__ = [
  'db', 
  'Game',
  'Genre', 
  'Platform',
  'RevokedToken'
  'User',
]

# You must import all of the new Models you create to this page

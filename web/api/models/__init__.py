# this file structure follows http://flask.pocoo.org/docs/1.0/patterns/appfactories/
# initializing db in api.models.base instead of in api.__init__.py
# to prevent circular dependencies
from .base import db
from .Game import Game
from .Genre import Genre
from .User import User
from .RevokedToken import RevokedToken

__all__ = [
  'db', 
  'Game',
  'Genre', 
  'User',
  'RevokedToken'
]

# You must import all of the new Models you create to this page

from .base import db
from sqlalchemy import or_
from .Genre import Genre
import string

game_genres = db.Table('game_genres',
  db.Column('game_id', db.Integer, db.ForeignKey('games.id'), primary_key=True),
  db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True),
  db.PrimaryKeyConstraint('game_id', 'genre_id')
)

game_platforms = db.Table('game_platforms',
  db.Column('game_id', db.Integer, db.ForeignKey('games.id'), primary_key=True),
  db.Column('platform_id', db.Integer, db.ForeignKey('platforms.id'), primary_key=True),
  db.PrimaryKeyConstraint('game_id', 'platform_id')
)

    

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    year = db.Column(db.Integer)
    genres = db.relationship(
        'Genre',
        secondary=game_genres,
        lazy='subquery',
        backref=db.backref('genres', lazy=True, cascade='all, delete')
        )
    platforms = db.relationship(
        'Platform',
        secondary=game_platforms,
        lazy='subquery',
        backref=db.backref('games', lazy=True, cascade='all, delete')
        )

    def __init__(self, title: str):
        self.title = title

    def __repr__(self):
        return f'<Game {self.title}>'
    
    @property
    def to_json(self):
        genres = []
        for genre in self.genres:
            genres.append(genre.to_json)
        platforms = []
        for platform in self.platforms:
            platforms.append(platform.to_json)
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'year': self.year,
            'genres': genres,
            'platforms': platforms
        }
        
    @classmethod
    def return_searchtitle(self, offset, limit, title):

        return {'games': [g.to_json for g in self.query\
                                .filter(Game.title.contains(title))\
                                .order_by(Game.id).offset(offset).limit(limit).all()]}
    @classmethod
    def return_all(self, offset, limit):
        return {'games': [g.to_json for g in self.query\
                                .join(Game.genres, aliased=True)\
                                .filter_by(id=2).order_by(Game.id).offset(offset).limit(limit).all()]}
    @classmethod
    def return_fgenres2(self, offset, limit, genres2):
        _query = self.query\
                      .join(Game.genres, aliased = True)
        genres3 = ''.join(i for i in genres2 if i.isdigit())
        for gid in genres3:
            _query = _query.filter(Genre.id.contains(genres3))
            
        _query = _query.order_by(Game.id).offset(offset).limit(limit)
        return {'games': [g.to_json for g in _query.all()]}        

    @classmethod
    def return_fgenres(self, offset, limit, genres2):
        _query = self.query\
                      .join(Game.genres, aliased = True)\
                      .filter(Genre.id.in_(genres2))\
                      .order_by(Game.id)\
                      .offset(offset)\
                      .limit(limit)
        return {'games': [g.to_json for g in _query.all()]}
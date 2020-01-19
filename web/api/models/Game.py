from .base import db
from sqlalchemy import or_
from .Genre import Genre
from .Platform import Platform
import string

game_genres = db.Table('game_genres',
                       db.Column('game_id', db.Integer, db.ForeignKey(
                           'games.id'), primary_key=True),
                       db.Column('genre_id', db.Integer, db.ForeignKey(
                           'genres.id'), primary_key=True),
                       db.PrimaryKeyConstraint('game_id', 'genre_id')
                       )

game_platforms = db.Table('game_platforms',
                          db.Column('game_id', db.Integer, db.ForeignKey(
                              'games.id'), primary_key=True),
                          db.Column('platform_id', db.Integer, db.ForeignKey(
                              'platforms.id'), primary_key=True),
                          db.PrimaryKeyConstraint('game_id', 'platform_id')
                          )


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    year = db.Column(db.Integer)
    image_url = db.Column(db.String)
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
        backref=db.backref('platforms', lazy=True, cascade='all, delete')
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
        ratings_sum = sum(map(lambda rating: rating.value, self.ratings))
        ratings_len = len(self.ratings)
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'year': self.year,
            'image_url': self.image_url,
            'genres': genres,
            'platforms': platforms,
            'ratings_count': ratings_len,
            'avarage_rating': None if ratings_len == 0 else round(ratings_sum / ratings_len, 2),
        }

    @classmethod
    def return_searchtitle(self, offset, limit, title):

        return {'games': [g.to_json for g in self.query
                          .filter(Game.title.contains(title))
                          .order_by(Game.id).offset(offset).limit(limit).all()]}

    @classmethod
    def return_searchtitle_genre(self, offset, limit, title, genres2):

        return {'games': [g.to_json for g in self.query
                          .join(Game.genres, aliased=True)
                          .filter(Genre.id.in_(genres2))
                          .filter(Game.title.contains(title))
                          .order_by(Game.id).offset(offset).limit(limit).all()]}

    @classmethod
    def return_searchtitle_platform(self, offset, limit, title, platform2):

        return {'games': [g.to_json for g in self.query
                          .join(Game.platforms, aliased=True)
                          .filter(Platform.id.in_(platform2))
                          .filter(Game.title.contains(title))
                          .order_by(Game.id).offset(offset).limit(limit).all()]}

    @classmethod
    def return_all(self, offset, limit):
        return {'games': [g.to_json for g in self.query
                          .order_by(Game.id).offset(offset).limit(limit).all()]}

    @classmethod
    def return_alls(self):
        _query = self.query\
            .order_by(Game.id)
        return _query

    @classmethod
    def return_byplatform(self, offset, limit, platform2):
        _query = self.query\
            .join(Game.platforms, aliased=True)\
            .filter(Platform.id.in_(platform2))\
            .order_by(Game.id)\
            .offset(offset)\
            .limit(limit)
        return {'games': [g.to_json for g in _query.all()]}

    @classmethod
    def return_bygenres(self, offset, limit, genres2):
        _query = self.query\
            .join(Game.genres, aliased=True)\
            .filter(Genre.id.in_(genres2))\
            .order_by(Game.id)\
            .offset(offset)\
            .limit(limit)
        return {'games': [g.to_json for g in _query.all()]}

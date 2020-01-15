from .base import db
from sqlalchemy import or_
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

#################################
####    Game DataModel Class
#################################   

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
    def return_searchtitle_genre(self, offset, limit, title, genres2):

        return {'games': [g.to_json for g in self.query\
                                .join(Game.genres, aliased = True)\
                                .filter(Genre.id.in_(genres2))\
                                .filter(Game.title.contains(title))\
                                .order_by(Game.id).offset(offset).limit(limit).all()]}
                                
    @classmethod
    def return_searchtitle_platform(self, offset, limit, title, platform2):

        return {'games': [g.to_json for g in self.query\
                                .join(Game.platforms, aliased = True)\
                                .filter(Platform.id.in_(platform2))\
                                .filter(Game.title.contains(title))\
                                .order_by(Game.id).offset(offset).limit(limit).all()]}
                                
    @classmethod
    def return_searchtitle_platform_genre(self, offset, limit, title, platform2, genres2):

        return {'games': [g.to_json for g in self.query\
                                .join(Game.platforms, aliased = True)\
                                .filter(Platform.id.in_(platform2))\
                                .join(Game.genres, aliased = True)\
                                .filter(Genre.id.in_(genres2))\
                                .filter(Game.title.contains(title))\
                                .order_by(Game.id).offset(offset).limit(limit).all()]}
                                
    @classmethod
    def return_all(self, offset, limit):
        return {'games': [g.to_json for g in self.query\
                                .order_by(Game.id).offset(offset).limit(limit).all()]}
    
    @classmethod
    def return_byplatform(self, offset, limit, platform2):
        _query = self.query\
                      .join(Game.platforms, aliased = True)\
                      .filter(Platform.id.in_(platform2))\
                      .order_by(Game.id)\
                      .offset(offset)\
                      .limit(limit)
        return {'games': [g.to_json for g in _query.all()]}                             

    @classmethod
    def return_bygenres(self, offset, limit, genres2):
        _query = self.query\
                      .join(Game.genres, aliased = True)\
                      .filter(Genre.id.in_(genres2))\
                      .order_by(Game.id)\
                      .offset(offset)\
                      .limit(limit)
        return {'games': [g.to_json for g in _query.all()]}
		
#################################
####    Genre DataModel Class
#################################        
class Genre(db.Model):
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'<Genre {self.name}>'

    @property
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    @property
    def to_json_dangerously(self):
        # https://gist.github.com/hest/8798884
        q = db.session.query(Genre).filter_by(id=self.id).join(Game.genres) 
        count = db.session.execute(q.statement.with_only_columns([db.func.count()]).order_by(None)).scalar()
        return {
            'id': self.id,
            'name': self.name,
            'count': count
        }


    @classmethod
    def return_all(cls):
        return {
            'data': list(map(lambda g: g.to_json_dangerously, Genre.query.all()))
        }

#################################
####    Platform DataModel Class
#################################   
class Platform(db.Model):
    __tablename__ = "platforms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'<Platform {self.name}>'

    @property
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    @property
    def to_json_dangerously(self):
        q = db.session.query(Platform).filter_by(id=self.id).join(Game.platforms)
        count = db.session.execute(q.statement.with_only_columns([db.func.count()]).order_by(None)).scalar()
        return {
            'id': self.id,
            'name': self.name,
            'count': count
        }

    @classmethod
    def return_all(cls):
        return {
            'data': list(map(lambda p: p.to_json_dangerously, Platform.query.all()))
        }		
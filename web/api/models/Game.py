from .base import db

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
    genres = db.relationship(
        'Genre',
        secondary=game_genres,
        lazy='subquery',
        backref=db.backref('games', lazy=True, cascade='all, delete')
    )
    platforms = db.relationship(
        'Platform',
        secondary=game_platforms,
        lazy='subquery',
        backref=db.backref('games', lazy=True, cascade='all, delete')
    )
    ratings = db.relationship('Rating', backref='game')

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
            'genres': genres,
            'platforms': platforms,
            'ratings_count': ratings_len,
            'avarage_rating': None if ratings_len == 0 else round(ratings_sum / ratings_len, 2),
        }

    @classmethod
    def return_by_id(self, id):
        game = self.query.filter_by(id=id).first()
        if game is None:
            return {'game': None}
        else:
            game = game.to_json
            game['user_rating'] = None  # TODO: Show user rating
            return {'game': game}

    @classmethod
    def return_all(self, offset, limit):
        return {'games': list(map(lambda g: g.to_json, self.query.order_by(Game.id).offset(offset).limit(limit).all()))}

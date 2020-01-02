from .base import db

game_genres = db.Table('game_genres',
  db.Column('game_id', db.Integer, db.ForeignKey('games.id'), primary_key=True),
  db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True),
  db.PrimaryKeyConstraint('game_id', 'genre_id')
)

class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    year = db.Column(db.Integer)
    genres = db.relationship(
        'Genre',
        secondary=game_genres,
        lazy='subquery',
        backref=db.backref('games', lazy=True)
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
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'year': self.year,
            'genres': genres,
        }

    @classmethod
    def return_all(cls):
        return {'data': list(map(lambda g: g.to_json, Game.query.all()))}
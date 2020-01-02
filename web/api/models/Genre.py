from .base import db

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
            'count': len(self.games)
        }

    @classmethod
    def return_all(cls):
        return {'data': list(map(lambda g: g.to_json, Genre.query.all()))}
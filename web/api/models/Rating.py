from sqlalchemy.sql import expression

from .base import db
from .Game import Game
from .User import User


class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    exclude_from_model = db.Column(db.Boolean, default=False, server_default=expression.false(), nullable=False)
    

    constraint = db.UniqueConstraint('game_id', 'user_id')

    def __repr__(self):
        return f'<Rating {self.id}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    @property
    def to_json(self):
        return {
            'id': self.id,
            'game_id': self.game_id,
            'user_id': self.user.id,
            'value': self.value,
            'exlude_from_model': self.exclude_from_model
        }

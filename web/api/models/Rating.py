from .base import db
from .Game import Game
from .User import User

class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)

    constraint = db.UniqueConstraint('game_id', 'user_id')
        
    def __repr__(self):
        return f'<Rating {self.id}>'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @property
    def to_json(self):
        return {
            'id': self.id,
            'value': self.value,
        }

    # @property
    # def to_json_dangerously(self):
    #     # https://gist.github.com/hest/8798884
    #     q = db.session.query(Genre).filter_by(id=self.id).join(Game.genres) #.filter(genre_id == self.id) #.filter(Games.id==1).count() filter(games = self.id)
    #     count = db.session.execute(q.statement.with_only_columns([db.func.count()]).order_by(None)).scalar()
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'count': count
    #     }


    @classmethod
    def return_all(cls):
        return {
            'data': list(map(lambda g: g.to_json, Rating.query.all()))
        }
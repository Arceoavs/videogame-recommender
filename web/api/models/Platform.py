from .base import db
#from .Game import Game


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
        q = db.session.query(Platform).filter_by(
            id=self.id).join(Game.platforms)
        count = db.session.execute(q.statement.with_only_columns(
            [db.func.count()]).order_by(None)).scalar()
        return {
            'id': self.id,
            'name': self.name,
            'count': count
        }

    @classmethod
    def return_all(cls):
        return {
            'platforms': list(map(lambda p: p.to_json_dangerously, Platform.query.all()))
        }

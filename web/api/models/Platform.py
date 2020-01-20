from .base import db


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
<<<<<<< HEAD
        q = db.session.query(Platform).filter_by(id=self.id)#.join(Game.platforms)
        #count = db.session.execute(q.statement.with_only_columns([db.func.count()]).order_by(None)).scalar()
=======
        q = db.session.query(Platform).filter_by(
            id=self.id).join(Game.platforms)
        count = db.session.execute(q.statement.with_only_columns(
            [db.func.count()]).order_by(None)).scalar()
>>>>>>> bc443ccf15850db1afbd251501bef13b52d115cc
        return {
            'id': self.id,
            'name': self.name,
            #'count': count
        }

    @classmethod
    def return_all(cls):
        return {
            'platforms': [p.to_json_dangerously for p in Platform.query.all()]
        }

from .base import db


class Genre(db.Model):
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name):
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
<<<<<<< HEAD
        q = db.session.query(Genre).filter_by(id=self.id)#.join(Game.genres) #.filter(genre_id == self.id) #.filter(Games.id==1).count() filter(games = self.id)
        #count = db.session.execute(q.statement.with_only_columns([db.func.count()]).order_by(None)).scalar()
=======
        q = db.session.query(Genre).filter_by(id=self.id).join(Game.genres)
        count = db.session.execute(q.statement.with_only_columns(
            [db.func.count()]).order_by(None)).scalar()
>>>>>>> bc443ccf15850db1afbd251501bef13b52d115cc
        return {
            'id': self.id,
            'name': self.name,
            #'count': count
        }

    @classmethod
    def return_all(self):
        return {
            'genres': [g.to_json_dangerously for g in self.query.all()]
        }

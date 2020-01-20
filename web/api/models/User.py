from passlib.hash import pbkdf2_sha256 as sha256
from .base import db


class User(db.Model):
    """User Table."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    ratings = db.relationship('Rating', backref='user')

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @property
    def to_json(self):
        ratings = []
        for rating in self.ratings:
            ratings.append(rating.to_json)
        return {
            'id': self.id,
            'username': self.username,
            'ratings': ratings,
        }

    @classmethod
    def return_by_username(cls, username):
        return {'user': cls.query.filter_by(username=username).first().to_json}

    @classmethod
    def return_all(cls):
        return {'users': [x.to_json for x in User.query.all()]}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

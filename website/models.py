from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    admin = db.Column(db.Boolean)


class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    photo = db.Column(db.BLOB)
    name = db.Column(db.String(150))
    date = db.Column(db.String(150))
    class_predict = db.Column(db.String(150))

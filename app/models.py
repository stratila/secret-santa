from app import db
from sqlalchemy.sql import expression
from secrets import token_hex


def generate_identifier():
    return token_hex(5)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    username = db.Column(db.String(64), index=True, unique=True)
    phone_number = db.Column(db.String(32), index=True, unique=True)
    address = db.Column(db.Text())
    present = db.Column(db.Text())
    state = db.Column(db.Integer)
    room = db.Column(db.Integer, db.ForeignKey('room.id'))
    # ready = db.Column(db.Boolean, server_default=expression.false(), nullable=False) #SQLite
    ready = db.Column(db.Boolean, server_default='f', default=False)  # Postgres (в SQLite тоже работает)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(64), default=generate_identifier, unique=True)
    owner_id = db.Column(db.Integer, unique=True)
    users = db.relationship('User', backref='participant', lazy='dynamic')



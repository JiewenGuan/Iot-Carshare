from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    bookings = db.relationship('Booking', backref='user',lazy='dynamic')
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    make = db.Column(db.String(64))
    body_type = db.Column(db.Integer)
    colour = db.Column(db.Integer)
    seats = db.Column(db.Integer)
    location = db.Column(db.String(64))
    rate = db.Column(db.Float)
    status = db.Column(db.Integer)
    bookings = db.relationship('Booking', backref='car',lazy='dynamic')

    def __repr__(self):
        return '<Car {}|{}>'.format(self.id,self.name)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timebooked = db.Column(db.DateTime, default=datetime.utcnow)
    timestart = db.Column(db.DateTime)
    dration = db.Column(db.Integer)
    timeend = db.Column(db.DateTime)
    status = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))

    def __repr__(self):
        return '<Booking {}|{}>'.format(self.user_id,self.car_id)

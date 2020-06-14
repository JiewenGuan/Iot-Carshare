"""
This module defines the data models that are usedby the database and served
by the API. There are three clases defining the three key data objects,
which are representative of the tables i the database.
"""

from app import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib


class User(db.Model):
    """
    Defines the model for a user and the CRUD commands available.
    This includes all classes of users as these are controlled via the
    role parameter.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index = True, unique = True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy='dynamic')
    face_token =  db.Column(db.String(128), index = True, unique = True)
    last_seen = db.Column(db.DateTime)
    mac_address = db.Column(db.String(128), unique = True)
    role = db.Column(db.Integer, nullable=False)

    def __init__(self, data):
        self.from_dict(data=data, new_user=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        if len(password) > 6:
            self.password_hash = generate_password_hash(password)
            return True
        else:
            return False

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email, 
            'role': self.role,
            'mac_address': self.mac_address
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username','email','mac_address']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])
        if 'role' in data:
            self.role = data['role']
        else:
            self.role = 2
        hashing = hashlib.sha256(self.username.encode("utf-8"))
        self.face_token = hashing.hexdigest()


class Car(db.Model):
    """
    Defines the model for a car and the CRUD commands available.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    make = db.Column(db.String(64))
    body_type = db.Column(db.Integer)
    colour = db.Column(db.Integer)
    seats = db.Column(db.Integer)
    location = db.Column(db.String(64))
    rate = db.Column(db.Float)
    status = db.Column(db.Integer)
    bookings = db.relationship('Booking', backref='car', lazy='dynamic')

    def __init__(self, data):
        self.from_dict(data=data)
    
    def __repr__(self):
        return '<Car {}|{}>'.format(self.id, self.name)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'name': self.name,
            'make': self.make,
            'body_type': self.body_type,
            'colour': self.colour,
            'seats': self.seats,
            'location': self.location,
            'rate': self.rate,
            'status': self.status
        }
        return data

    def from_dict(self, data):
        for field in data:
            setattr(self, field, data[field])

    


class Booking(db.Model):
    """
    Defines the model for a booking and the CRUD commands available.
    """
    id = db.Column(db.Integer, primary_key=True)
    timebooked = db.Column(db.DateTime, default=datetime.now)
    timestart = db.Column(db.DateTime)
    dration = db.Column(db.Integer)
    timeend = db.Column(db.DateTime)
    status = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))

    def __init__(self,data):
        self.from_dict(data)

    def __repr__(self):
        return '<Booking {}|{}>'.format(self.user_id, self.car_id)
    
    def from_dict(self, data):
        self.user_id = data['user_id']
        self.car_id = data['car_id']
        self.dration = data['hours']
        self.timestart = datetime.fromisoformat(data['time_start'])
        self.timeend = self.timestart + timedelta(hours=self.dration)
        if 'status' in data:
            self.status = data['status']
    
    def to_dict(self):
        data={
            'id' : self.id,
            'timebooked' : self.timebooked.isoformat(),
            'timestart' : self.timestart.isoformat(),
            'dration' : self.dration,
            'timeend' : self.timeend.isoformat(),
            'status' : self.status,
            'user_id' : self.user_id,
            'car_id' : self.car_id,
        }
        return data


if __name__ == "__main__":
    pass
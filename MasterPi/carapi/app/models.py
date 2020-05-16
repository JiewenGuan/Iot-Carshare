from app import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    bookings = db.relationship('Booking', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            #'password_hash': self.password_hash
            #'bookings': url_for('get_user_bookings', id=self.id),
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])


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
    bookings = db.relationship('Booking', backref='car', lazy='dynamic')
    
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
            #'bookings': url_for('get_car_bookings', id=self.id),
        }
        return data

    def from_dict(self, data):
        for field in data:
            setattr(self, field, data[field])

    


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timebooked = db.Column(db.DateTime, default=datetime.now)
    timestart = db.Column(db.DateTime)
    dration = db.Column(db.Integer)
    timeend = db.Column(db.DateTime)
    status = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))

    def __repr__(self):
        return '<Booking {}|{}>'.format(self.user_id, self.car_id)
    
    def from_dict(self, data):
        self.user_id = data['user_id']
        self.car_id = data['car_id']
        self.dration = data['hours']
        self.timestart = datetime.fromisoformat(data['time_start'])
        self.timeend = self.timestart + timedelta(hours=self.dration)
    
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

from app import app, db
from app.models import User, Car, Booking
from flask import jsonify, request, url_for
from sqlalchemy import and_
from werkzeug.http import HTTP_STATUS_CODES
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/uniq/<string:name>', methods=['GET'])
def uniq_name(name):
    user = User.query.filter_by(username=name).first()
    if user is not None:
        return bad_request('use a different name')
    return jsonify(User(username=name).to_dict())

@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json() or {}
    if 'username' not in data or 'password' not in data:
        return bad_request('500 must include username and password fields')
    user = User.query.filter_by(username=data['username']).first()
    if user:
        if user.check_password(data['password']):
            return jsonify(user.to_dict())
    return bad_request('wrong username or password!')

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list_to_dict(User.query.all()))

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'password' not in data:
        return bad_request('must include username and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 200
    response.headers['Location'] = url_for('get_user', id=user.id)
    return response

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())

@app.route('/cars/<int:id>', methods=['GET'])
def get_car(id):
    return jsonify(Car.query.get_or_404(id).to_dict())

@app.route('/cars', methods=['GET'])
def get_cars():
    my_filters = request.get_json() or {}
    query = db.session.query(Car)

    for attr,value in my_filters.items():
        query = query.filter(getattr(Car,attr)==value)
    
    return jsonify(list_to_dict(query.all()))

@app.route('/cars', methods=['POST'])
def create_car():
    data = request.get_json() or {}
    if 'name' not in data :
        return bad_request('500 must include name')
    
    car = Car()
    car.from_dict(data)
    db.session.add(car)
    db.session.commit()
    response = jsonify(car.to_dict())
    response.status_code = 200
    response.headers['Location'] = url_for('get_car', id=car.id)
    return response

@app.route('/cars/<int:id>', methods=['PUT'])
def update_car(id):
    car = Car.query.get_or_404(id)
    data = request.get_json() or {}
    
    car.from_dict(data)
    db.session.commit()
    return jsonify(car.to_dict())

@app.route('/bookings/<int:id>', methods=['GET'])
def get_booking(id):
    return jsonify(Booking.query.get_or_404(id).to_dict())

@app.route('/bookings', methods=['GET'])
def get_bookings():
    return jsonify(list_to_dict(Booking.query.all()))

@app.route('/user_bookings/<int:id>')
def user_bookings(id):
    query = db.session.query(Booking).filter(Booking.user_id == id)
    return jsonify(list_to_dict(query.all()))

@app.route('/cancel_booking/<int:id>')
def cancel_booking(id):
    b = Booking.query.get(id)
    if b is None or b.status !=1:
        return bad_request("booking not exist or inactive")
    if b.timestart < datetime.now():
        return bad_request("cannot cancel, session already started")
    b.status = 0
    c = Car.query.get(b.car_id)
    c.status = 1
    db.session.commit()
    return jsonify(b.to_dict())

@app.route('/return_booking/<int:id>/<string:loc>')
def return_booking(id, loc):
    b = Booking.query.get(id)
    if b is None or b.status !=1:
        return bad_request("booking not exist or inactive")
    if b.timestart > datetime.now():
        return bad_request("session havn't start, cannot return, try cancel")
    b.status = 2
    b.timeend = datetime.now()
    c = Car.query.get(b.car_id)
    c.status = 1
    c.location = loc
    db.session.commit()
    return jsonify(b.to_dict())

@app.route('/book', methods=['POST'])
def book():
    data = request.get_json() or {}
    if 'user_id' not in data or 'car_id' not in data or 'time_start' not in data or 'hours' not in data:
        return bad_request('some fields are missing')
    car = Car.query.get(data['car_id'])
    if car.status != 1:
        return bad_request('the car is not avaliable now')
    car.status = 2
    booking = Booking()
    booking.from_dict(data)
    booking.status = 1
    db.session.add(booking)
    db.session.commit()
    response = jsonify(booking.to_dict())
    response.status_code = 200
    response.headers['Location'] = url_for('get_booking', id=booking.id)
    return response


def bad_request(message):
    return error_response(400, message)

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response













def list_to_dict(list):
    ret = []
    for i in list:
        ret.append(i.to_dict())
    return ret
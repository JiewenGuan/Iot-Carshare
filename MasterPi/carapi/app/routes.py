from app import app, db
from app.models import User, Car, Booking
from flask import jsonify, request, url_for

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

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
        return '500 must include username and password fields'
    if User.query.filter_by(username=data['username']).first():
        return '500 please use a different username'
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















def list_to_dict(list):
    ret = []
    for i in list:
        ret.append(i.to_dict())
    return ret
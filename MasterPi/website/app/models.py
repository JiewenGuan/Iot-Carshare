from flask_login import UserMixin
import requests
from app import login

class User(UserMixin):

    def __init__(self, username, id):
        self.username = username
        self.id = id


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
        }
        return data
        

@login.user_loader
def load_user(id):
    r = requests.get('https://192.168.1.109:10100/users/{}'.format(id), verify=False)
    retdata = r.json() or {}
    return User(username=retdata['username'],id=retdata['id']) 
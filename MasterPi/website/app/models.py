from flask_login import UserMixin
import requests
from app import login
from flask import session

class User(UserMixin):

    def __init__(self, username, id, role):
        self.username = username
        self.id = id
        self.role = role

@login.user_loader
def load_user(id):
    r = requests.get('http://192.168.1.109:10100/users/{}'.format(id), verify=False)
    retdata = r.json() or {}
    if 'error' in retdata:
        return None
    return User(username=retdata['username'],id=retdata['id'],role=retdata['role'])  

class Car():
    
    def __init__(self):
            self.body_type= None
            self.colour=None
            self.id=None
            self.location= ""
            self.make= ""
            self.name= ""
            self.rate= None
            self.seats= None
            self.status= None


    def from_dict(self, data):
        for field in data:
            setattr(self, field, data[field])

        

    
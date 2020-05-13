import os
class Config(object):
    REST_SERVER = '192.168.1.109:5000'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

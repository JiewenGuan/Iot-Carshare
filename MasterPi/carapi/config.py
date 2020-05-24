import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    HOST = "35.197.181.169"
    USER = "root"
    PASSWORD = "asdqwe123"
    DATABASE = "People"
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #SQLALCHEMY_DATABASE_URI ="mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

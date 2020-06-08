import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    HOST = "35.197.165.251"
    USER = "root"
    PASSWORD = "3dE3GoPn9tKP7kjm"
    DATABASE = "carshare"
    
    SECRET_KEY = 'asdqwhret0qwiufgn0wefrh0er'
    SQLALCHEMY_DATABASE_URI ="mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)

    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        #'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

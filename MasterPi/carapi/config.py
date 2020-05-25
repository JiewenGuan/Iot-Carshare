import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """
    Configuration variables for the database connection.
    """
    HOST = "35.197.181.169"
    USER = "root"
    PASSWORD = "asdqwe123"
    DATABASE = "Carshare"
    
    SECRET_KEY = 'asdqwhret0qwiufgn0wefrh0er'
    SQLALCHEMY_DATABASE_URI ="mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)

    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        #'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


if __name__ == "__main__":
    pass
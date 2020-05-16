import os
class Config(object):
    REST_SERVER = '192.168.1.109:5000'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    CAR_COLORS = ['Color','red','green','blue','yello','white','black']
    BODY_TYPE = ['Body Type','sedan','truck','van','pickup','suv']
    CAR_STATUSES = ['in service', 'avaliable', 'booked']
    BOOKING_STAT = ['canceled', 'active', 'returned']

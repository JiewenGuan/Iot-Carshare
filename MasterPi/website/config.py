import os
class Config(object):
    REST_SERVER = '192.168.1.109:5000'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'new-key'
    CAR_COLORS = ['Color','red','green','blue','yello','white','black']
    BODY_TYPE = ['Body Type','Sedan','Truck','Van','Pickup','Suv','Other']
    CAR_STATUSES = ['in service', 'avaliable', 'booked']
    BOOKING_STAT = ['canceled', 'active', 'returned', 'service']
    USER_TYPE = ['Admin','Engeneer','Customer']

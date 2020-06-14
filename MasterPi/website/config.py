"""
This module's purpose is to contain the class for storing Flask configuration information.
"""
import os


class Config(object):
    """
    Configuration class for Flask with keys as class level variables
    for data structures, server IP, booking information .etc

    .. note:: It is important to define an environment variable for the
        SECRET_KEY variable if deploying this publicly as the default key
        is not secure.
    """

    REST_SERVER = '192.168.1.109:5000'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'new-key'
    CAR_COLORS = ['Color','red','green','blue','yello','white','black']
    BODY_TYPE = ['Body Type','Sedan','Truck','Van','Pickup','Suv','Other']
    CAR_STATUSES = ['in service', 'avaliable', 'booked']
    BOOKING_STAT = ['canceled', 'active', 'returned', 'service']
    USER_TYPE = ['Admin','Engeneer','Customer','Manager']

if __name__ == "__main__":
    pass
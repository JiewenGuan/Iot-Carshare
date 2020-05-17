# For the consistant usage of Agent Data.
# Might not be neccessary

"""
At this stage, I am trying to pass in the car object to the validation module
so that the main module no longer has control over it. DONE
There is no reason for the main module to know who just used the 
vehicle, so this reduces the need for the main module to know more
than the car that it is operating in. DONE
As such, I should move the information from main to validation, or as much 
as is possible. DONE
This way, if a valid user is loaded, then the car can be passed into
the operational section for any usage of the variables. This SHOULD
remove the need for a carlocked variable.... DONE
"""
 
import datetime
import dateutil.parser
# TODO This code is adapted from https://pynative.com/python-serialize-datetime-into-json/
# TODO This code requires the dateutil package - install by pip3 install python-dateutil

# This class is used to construct a dictionary for passing over sockets.
# It must be instantiated with all the parameters, though parameters 
# can be None - this is used to interpret the intent of the socket connection.
# Its primary method returns a dictionary constructed in a consistent way.
class DictionaryConstructor:
    # Remember to only instantiate this class by setting the constructors
    # appropriately to the request. 
    # # 
    def __init__(
        self, 
        car_id: str, 
        username: str, 
        password: str, 
        usertoken: str, 
        info_date_time: str,
        current_location: tuple):

        self.car_id = car_id
        self.username = username
        self.password = password
        self.usertoken = usertoken
        self.info_date_time = info_date_time
        self.current_location = current_location

    def get_socket_dictionary(self) -> dict:
        socket_dictionary = {
            "car_id": self.car_id,
            "username": self.username,
            "password": self.password,
            "usertoken": self.usertoken,
            "info_date_time": self.info_date_time,
            "current_location": self.current_location
        }
        return socket_dictionary

# Accepts an ISO format date and returns a python date object.
class DictionaryDateUpdater:
    def __init__(self, isodate: str):
        self.isodate = isodate

    def get_python_date(self):
        return dateutil.parser.parse(self.isodate)

if __name__ == "__main__":
    date_time_tosend = datetime.datetime.now()
    print(date_time_tosend)
    date_time_tosend = date_time_tosend.isoformat()
    test_dict = DictionaryConstructor(
        "IDofCar", 
        "users_name", 
        None,
        "users_token",
        date_time_tosend,
        (123.123, 234.234)
        )
    test_send = test_dict.get_socket_dictionary()
    print(test_send)
    # Doesn't work in python 3.5 on raspberry pi - only 3.7 or newer.
    # Use this if the raspberri pi is updated to 3.7 - it is reduces reliance
    # on third party packages.
    #test_send["info_date_time"] = datetime.fromisoformat(test_send["info_date_time"])
    update_dictionary = DictionaryDateUpdater(test_send["info_date_time"])
    test_send["info_date_time"] = update_dictionary.get_python_date()
    print("Returned Object: {}".format(test_send["info_date_time"]))
    print(test_send)
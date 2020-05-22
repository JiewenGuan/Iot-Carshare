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
    # def __init__(
    #     self, 
    #     action: int,
    #     car_id: str, 
    #     username: str, 
    #     password: str, 
    #     usertoken: str, 
    #     info_date_time: str,
    #     current_location: tuple
    #     ):

    #     self.action = action
    #     self.car_id = car_id
    #     self.username = username
    #     self.password = password
    #     self.usertoken = usertoken
    #     self.info_date_time = info_date_time
    #     self.current_location = current_location

    # Updated constructor only accepts the mandatory values and returns 
    # the dictionary to updated as needed.
    def __init__(
            self, 
            car_id: str, 
            info_date_time: str
    ):

        self.action = None
        self.car_id = car_id
        self.username = None
        self.password = None
        self.usertoken = None
        self.info_date_time = info_date_time
        self.current_location = None

    # Setters for the dictionary beyond the constructor:
    # This is implemented so that the dictionary can be expanded as necessary.
    # Alternatively we could construct an empty dictionary and modify the
    # values based on keys, but this would require significant code changes
    # when accessing the values if the keys change. Also allows us to make
    # changes to the data if needed.
    def set_action(self, action: str):
        self.action = action
    
    def set_username(self, username: str):
        self.username = username
    
    def set_password(self, password: str):
        self.password = password
    
    def set_usertoken(self, usertoken: str):
        self.usertoken = usertoken

    def set_current_location(self, current_location: tuple):
        self.current_location = current_location

    # Returns the dictionary - should be called once the dictionary is constructed.
    def get_socket_dictionary(self) -> dict:
        socket_dictionary = {
            "action": self.action,
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
    def __init__(self, iso_date: str):
        self.iso_date = iso_date

    def get_python_date(self):
        return dateutil.parser.parse(self.iso_date)


if __name__ == "__main__":
    date_time_to_send = datetime.datetime.now()
    print(date_time_to_send)
    date_time_to_send = date_time_to_send.isoformat()
    # test_dict = DictionaryConstructor(
    #     1,
    #     "IDofCar", 
    #     "users_name", 
    #     None,
    #     "users_token",
    #     date_time_to_send,
    #     (123.123, 234.234)
    #     )
    test_dict = DictionaryConstructor(
        "IDofCar", 
        date_time_to_send,
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
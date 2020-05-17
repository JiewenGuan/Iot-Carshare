# This module contains the classes that are used to
# communicate with the master pi.

# Instantiating the class has accepts one paramter - the car_id. 
# The socket connection then sends a pickled object to the server.
# This object is defined at both ends, and is a dictionary that contains
# the car_id and the current time, as well as either of the username 
# and password (text validation) or the user_token (face validation).

# The two entry points for validation accept either the token from the face recognition file
# or the username and password (or equivalent) and then return the username or
# token respectively. The token is returned so that it can be used for future encoding
# of the pickle face recognition encoding file.

# The other entry point accepts nothing, and simply informs the master
# pi that the vehicle has been returned.


# might be appropriate to move these classes into one class and call the function.

# Validate the text credentials 

import socket
import ssl
import json
import time
from agentdata import DictionaryConstructor as DictionaryConstructor
from agentdata import DictionaryDateUpdater as DictionaryDateUpdater
import datetime
# from Crypto.Cipher import AES

# This class is instantiated with just the car_id and then the appropriate method
# must be called to achieve the desired result, passing in the appropriate
# objects. A dictionary is then constructed and returned using the agentdata.py
# module and then this is passed to the socket which returns a dictionary
# for the called method to act on
class SocketConnection:
    def __init__(self, car_id: str):
        self.car_id = car_id

        self.IP_ADDRESS = "127.0.0.1"
        self.M_PI_PORT = 33333

    # This function will send the username, password, car_id and date to
    # the server for validation.
    def validate_text_credentials(self, username: str, password: str):
        # Construct the dictionary
        socket_dictionary_creator = DictionaryConstructor(
            self.car_id, 
            username, 
            password, 
            None, 
            datetime.datetime.now().isoformat(),
            None)
        socket_dictionary = socket_dictionary_creator.get_socket_dictionary()
        print("socket dictionary returned")
        print(socket_dictionary)

        # Accept the returned dictionary from the socket communication.
        socket_return = self.establish_connection(socket_dictionary)

        # Process the dictionary and return based on the outcome.

        # For testing only. In reality the username is returned from the server as 
        # confirmation that a booking is valid at the time.
        if username == password:
            return True
        return False

    # Validate the face recognition.
    def validate_face_credentials(self, user_token: str):
        print("[TEST] validating {}".format(user_token))


    # class for updating the Master Pi when the booking has been concluded
    def terminate_booking(self):
        pass

    # This method is called by the methods in this class for performing
    # an action with the master pi. It accepts a dictionary (from agentdata)
    # and returns a dictionary of the same type to be acted on.
    def establish_connection(self, dict_to_send: dict) -> dict:
        # Convert the dictionary to a string json string object in utf-8.
        # This ensure that almost all special characters are preserved.
        encoded_dictionary = json.dumps(dict_to_send).encode("utf-8")

        # Open a socket and send the dictionary, then await a reply.
        returned_bytes = b""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((IP_ADDRESS, M_PI_PORT))
            print("Connected to Master")
            s.sendall(encoded_dictionary)
            
            # Recieve the data
            # TODO How do we exit this in a timely manner?
            while True:
                print("receiving datum")
                temporary_bytes = s.recv(1024)
                returned_bytes += temporary_bytes
        # Exit the context manager, closing the connection and convert
        # the bytes back to a dictionary.
        returned_dictionary = json.loads(returned_bytes.decode("utf-8"))
        print(returned_dictionary)

        # Update the returned dictionary to conform with the communication
        # standard, in case a date has been communicated in an ISO
        # format and return to the calling function.
        if returned_dictionary["info_date_time"] is not None:
            print("Updating Socket Dictionary")
            try: 
                update_dictionary = DictionaryDateUpdater(returned_dictionary["info_date_time"])
                returned_dictionary["info_date_time"] = update_dictionary.get_python_date()
            except as e:
                print("Error converting dictionary!")
                print(e)
        return returned_dictionary

if __name__ == "__main__":
    pass


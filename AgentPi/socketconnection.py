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
import pickle
import time
from Crypto.Cipher import AES


class SocketConnection:
    def __init__(self, car_id: str):
        self.car_id = car_id

        IP_ADDRESS = "127.0.0.1"
        MPI_PORT = 33333

    def validate_text_credentials(self, username: str, password: str):
        
        # accept_credentials(self, username: str, password: str, car_id: str) -> bool:
        # This function will send the username, password and the car_id to
        # the server for validation.


        # For testing only. In reality the username is returned from the server as 
        # confirmation that a booking is valid at the time.
        if username == password:
            return True
        return False



    # Validate the face recognition.
    def validate_face_credentials(self, user_token: str):
        print("[TEST] validating {}".format(user_token))


    # class for updating the Master Pi when the booking has been concluded
    def logout(self):
        pass

    def establish_connection(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP_ADDRESS, MPI_PORT))



if __name__ == "__main__":
    pass


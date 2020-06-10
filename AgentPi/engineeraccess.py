"""
This module provides functionality associated
with the acccess levels an engineer may need.
It is called once an engineer is validated and
control persists here on in classes called from 
this module until the engineer logs out.
"""

import time

# To consolidate logs into one location.
import logging
log = logging.getLogger(__name__)



class EngineerAccess():
    """
    The main class is constructed with the dictionary that was returned
    by the socket connection from the master pi. It has a single entry point
    of unlock_car that acts based on the dictionary that the class was 
    instantiated with.
    """

    def __init__(self, unlocked_car: dict):
        self.unlocked_car = unlocked_car

    def unlock_car(self):
        """
        Perform functions for unlocking the car for an engineer.
        """
        engineer_in_car = True
        while engineer_in_car:
            current_username = self.unlocked_car["username"]
            print("Engineer Access.")
            print("Welcome {}".format(current_username))
            print("Please select from the following options:\n \
            1. End Maintenance and lock the Car.")
            user_choice = input("Enter your choice: ")

            if user_choice == "1":
                # TODO how do we update the master if the connection fails?
                socket_connection = SocketConnection(self.unlocked_car["car_id"])

                # TODO get QR code.

                # Validate the QR code.

                # if valid do the following
                socket_connection.terminate_engineer()
                engineer_in_car = False
                # if invalid, inform and loop.
            time.sleep(1)
            os.system("clear")
        return

if __name__ == "__main__":
    pass
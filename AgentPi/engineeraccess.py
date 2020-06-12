"""
This module provides functionality associated
with the acccess levels an engineer may need.
It is called once an engineer is validated and
control persists here on in classes called from 
this module until the engineer logs out.
"""

import time

import qrreader
import utilities
# To consolidate logs into one location.
import logging
log = logging.getLogger(__name__)



class EngineerAccess():
    """
    The :class:`EngineerAccess` class is constructed with the dictionary that was returned
    by the socket connection from the master pi. It has a single entry point
    of :func:`unlock_car` that acts based on the dictionary that the class was 
    instantiated with.
    """

    def __init__(self, unlocked_car: dict):
        self.unlocked_car = unlocked_car

    def unlock_car(self):
        """
        Perform functions for unlocking the car for an engineer.
        Presents a single option which is to conclude
        the work, requring the engineer has a QR code for ID 
        purposes. If the logout attempts fail after a set number of times,
        the car locks for security reasons.
        """

        current_username = self.unlocked_car["username"]
        print("Engineer Access.")
        print("Welcome {}.".format(current_username))

        # Loop exit variables.
        engineer_in_car = True
        logout_attempts = 0
        failed_logouts = 3

        # Loop through the GUI.
        while engineer_in_car:
            # current_username = self.unlocked_car["username"]
            # print("Engineer Access.")
            # print("Welcome {}".format(current_username))
            print("Please select from the following options:\n \
            1. End Maintenance and lock the vehicle.")
            user_choice = input("Enter your choice: ")

            if user_choice == "1":

                # Search for the engineers QR code and
                # if it is of valid type, return the vehicle.
                qr_reader = qrreader.QRReader()
                engineer_code = qr_reader.read_qr_code()

                # If the code is returned, pass it to the socket.
                if engineer_code:
                    # TODO how do we update the master if the connection fails?
                    socket_connection = SocketConnection(self.unlocked_car["car_id"])
                    # Pass in the qr code to the socket connection and await a return.
                    car_returned = socket_connection.terminate_engineer(engineer_code)
                    engineer_in_car = False
                elif logout_attempts >= failed_logouts:
                    print("Exceeded logout attempts - locking vehicle for security purposes.")
                    time.sleep(3)
                    engineer_in_car = False
                else: 
                    print("No valid code found.")
                    logout_attempts += 1
                    time.sleep(2)
                # if invalid, inform and loop.
            else:
                print("Invalid Choice!\n")
                time.sleep(3)
                clear_util = utilities.HelperUtilities()
                clear_util.clear_keyboard()
                # os.system("clear")
        return

if __name__ == "__main__":
    pass
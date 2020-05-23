# This module contains the functionality that a user is offered when a
# car is unlocked.

import os
from socketconnection import SocketConnection
#from getpass import getpass
import hashlib
from facecapture import FaceCapture
from faceencoder import FaceEncoder
import time

# To consolidate logs into one location.
import logging
log = logging.getLogger(__name__)


# The main class is constructed with the dictionary that was returned
# by the socket connection from the master pi. It has a single entry point
# of unlock_car that acts based on the dictionary that the class was 
# instantiated with.
class UnlockedCar():
    def __init__(self, unlocked_car: dict):
        self.unlocked_car = unlocked_car

    # Perform functions for unlocking the car.
    def unlock_car(self):
        # GUI Loop.
        in_booking = True
        while in_booking:
            current_username = self.unlocked_car["username"]
            print("Welcome {}".format(current_username))
            print("Please select from the following options:\n \
            1. Return the Car.")
            # print("9. Update face recognition profile.")
            user_choice = input("Enter your choice: ")

            if user_choice == "1":
                # TODO how do we update the master if the connection fails?
                socket_connection = SocketConnection(self.unlocked_car["car_id"])
                socket_connection.terminate_booking()
                in_booking = False
            elif user_choice == "9":
                # Confirm the user's intent after warnings.
                print("Warning: Continuing will remove your existing face profile for this vehicle!")
                confirmation = input("Enter \"f\" to continue or any other choice to cancel: ")
                if confirmation != "f":
                    os.system("clear")
                    continue

                os.system("clear")
                print("Look directly at the camera for 15 seconds")

                # Update the user's face: 
                # In future if the MasterPi has the resources, it may be better to
                # 1. Prompt for a password. If this password is valid, the 
                # Master Pi will respond with a token which is then passed to the 
                # face recognition creator for creation. For exanple: 
                # print("To update your face recognition profile, please re-enter your password.")
                # password = getpass()

                # In this implementation, we simply call the FR software, updating
                # the faces in the user's folder and then updatating the pickle file.
                # This uses an agreed upon token - the hash of the username.
                hashing = hashlib.sha256(current_username.encode("utf-8"))
                user_token = hashing.hexdigest()
                log.info("Hashed username({}): {}".format(current_username, user_token))
                faces_folder = "data_folder"
                face_pickle = "face_encodings.pickle"

                # Instantiate the FaceCapture object and attempt to capture
                # a face. If this is successful, re_encode the pickle file.
                face_capture = FaceCapture(user_token, faces_folder)
                capture_success = face_capture.capture_face()
                if capture_success:
                    print("Encoding Faces - please wait....")
                    face_encoder = FaceEncoder(faces_folder, face_pickle)
                    encoding_success = face_encoder.encode_faces()
                    if encoding_success:
                        print ("Faces Encoded!")
                    else: 
                        print("Encoding Error - this error has been logged.")
                        log.exception("Encoding error with current dataset.")
                else:
                    print("Unable to capture adequate face images.")

            time.sleep(3)
            os.system("clear")
        return
    
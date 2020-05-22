# This class is responsible for accepting a user verification/validation
# choice, and then validating the user. If the user is validated, control
# is passed to a class that controls the vehicle (should this be the 
# intended action), else control is passed back to main.

from getpass import getpass
import sys
import time

from socketconnection import SocketConnection
import cardetails as CarDetails
from facerecognition import FaceRecognition
# To consolidate logs into one location.
import logging
log = logging.getLogger(__name__)


# Validation entrypoint. This can only be operated on when instantiated.
# This reduces unwarranted use of the validation function
class ValidateUser:
    
    # The init does the usual, but the userselection is the key as it 
    # assists the validatecredentials function in determining which
    # validate technique to use.
    def __init__(self, userselection: int, current_car: CarDetails):
        self.userselection = userselection
        self.current_car = current_car
        # self.validateCredentials()
        # print("is this executing?")
        log.info("Current Car in init: {}".format(self.current_car))
        self.socket_connection = SocketConnection(self.current_car.get_car_id())

    # Solely for directing the users choice to the appropriate function.
    # Returns false if an invalid choice is made, otherwise returns
    # true to indicate a return to the base state.
    def validateCredentials(self) -> bool:
        # print("User Choice: {choice}".format(choice = self.userselection))
        if self.userselection == "1":
            self.validate_text()
            return True
        elif self.userselection == "2":
            self.validate_face()
            return True
        else:
            return False

    # Validates user's text credentials. Returns after the number of attempts
    # is exceeded or the user was true and the car has been returned..
    def validate_text(self):
        attempts = 3
        #is_valid_user = False
        while attempts > 0:
            username = input("\nPlease enter your log in details: \nUsername: ")
            password = getpass()

            # Call validation function - validation function should return a boolean
            # if invalid credentials, None if there was an error, and the car if successful.
            # eventually the boolean is returned 
            print("Validating credentials....")
            # TODO test whether it is necessary to clear the keyboard input....
            returned_dict = self.socket_connection.validate_text_credentials(username, password)
            
            log.info("Returned_dict: {}".format(returned_dict))
            # Check if the connection returned a result, if not inform.
            # TODO This could be moved to its own function so that both validation functions can call it.
            if returned_dict is None:
                print("Unable to connect to Server - try again later.")
                time.sleep(3)
                continue

            # Progressing this far means the result was a dictionary or False.
            # Unlock the car and break, so when the car is locked and
            # control is returned to this function, the program returns
            # to the main menu.
            if returned_dict is not False:
                # self.current_car.currenuser = username
                # Action unlock. From here all actions during a booking should take
                # place in and throughout this function call.
                # Return to the main menu. (cascades back through calling functions)

                # TODO Temporary - the unlock function called should be passed the 
                # the username to unlock the car.
                #self.current_car.unlock_car(username)
                self.current_car.unlock_car(returned_dict)
                break
            
            # decrement attempts and inform the user.
            attempts = attempts - 1
            print ("Credentials invalid for this car at this time!\n\
            Attempts remaining: {remains}".format(remains = attempts))

            
    # Attempts to validate a face detection. Instantiates and calls the 
    # facerecognition.py which accepts one parameter, the location of the 
    # encodings file (pickle).
    def validate_face(self):
        face_validator = FaceRecognition("face_encodings.pickle")
        user_token = face_validator.recognise_face()

        # The previous call returns None if no match was found. Otherwise,
        # the token is passed to the socket_connection call to validate
        # the booking - see socketconnection for return details, and above code in 
        # credentials validation for example.
        if user_token is not None:
            print("Validating Booking.... {}".format(user_token))
            returned_dict = self.socket_connection.validate_face_credentials(user_token)
            log.info("returned_dict: {}".format(returned_dict))
            if returned_dict is None:
                print("Unable to connect to Server - try again later.")
                time.sleep(3)
                return
            if returned_dict is not False:
                # Action unlock. From here all actions during a booking should take
                # place in and throughout this function call.
                # Return to the main menu when done (cascades back through calling functions).
                self.current_car.unlock_car(returned_dict)
            else:
                print("Booking not found.")
                time.sleep(3)
        else:
            print("Face not recognised!\nPlease login with credentials.")
        time.sleep(2)


# For testing purposes.
if __name__ == "__main__":
    pass
    #main(sys.argv)
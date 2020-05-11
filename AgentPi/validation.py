# This class is responsible for accepting a user verification/validation
# choice, and then validating the user. If the user is validated, control
# is passed to a class that controls the vehicle (should this be the 
# intended action), else control is passed back to main.

from getpass import getpass
import sys
from socketconnection import SocketConnection
import cardetails as CarDetails
from facerecognition import FaceRecognition

import time

# Validation entrypoint. This can only be operated on when instantiated.
# This reduces unwarranted use of the validation function
class validateUser:
    
    # The init does the usual, but the userselection is the key as it 
    # assists the validatecredentials function in determining which
    # validate technique to use.
    def __init__(self, userselection: int, current_car: CarDetails):
        self.userselection = userselection
        self.current_car = current_car
        #self.validateCredentials()
        #print("is this executing?")
        print(self.current_car)
        self.socket_connection = SocketConnection(self.current_car.getCarID())

    # Solely for directing the users choice to the appropriate function.
    # Returns false if an invalid choice is made, otherwise returns
    # true to indicate a return to the base state.
    def validateCredentials(self) -> bool:
        #print("User Choice: {choice}".format(choice = self.userselection))
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
        is_valid_user = False
        while attempts > 0:
            username = input("\nPlease enter your username: ")
            
            password = getpass()

            # Call validation function - validation function should return a boolean
            # then the boolean can be used to action the unlock functions.
            # eventually the boolean is returned 
            print("Validating credentials....")
            #TODO test whether it is necessary to clear the keyboard input....
            is_valid_user = self.socket_connection.validate_text_credentials(username, password)

            if is_valid_user:
                
                # Action unlock. From here all actions during a booking should take
                # place in and throughout this function call.
                # Return to the main menu. (cascades back through calling functions)

                # TODO Temporary - the unlock function called should be passed the 
                # the username to unlock the car.
                self.current_car.unlock_car(username)
                print("Car Unlocked!")
                break
            
            # decrement attempts and inform the user.
            attempts = attempts - 1
            print ("Credentials invalid for this car at this time!\n\
            Attempts remaining: {remains}".format(remains = attempts))

            

            

        


    # Attempts to validate a face detection. Instantiates and calles the 
    # facerecognition.py which accepts one parameter, the location of the 
    # encodings file (pickle).
    def validate_face(self):
        face_validator = FaceRecognition("testpickle.pickle")
        user_token = face_validator.recognise_face()

        if user_token is not None:
            print("Validating Booking.... {}".format(user_token))
            self.socket_connection.validate_face_credentials(user_token)
        time.sleep(2)


if __name__ == "__main__":

    pass
    #main(sys.argv)
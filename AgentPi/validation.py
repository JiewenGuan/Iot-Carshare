"""
This class is responsible for accepting a user verification/validation
choice, and then validating the user. If the selection is valid, the 
appropriate user input is sought via a call to the designated function, 
else control is returned to the calling function.
"""
from getpass import getpass
import sys
import time

from socketconnection import SocketConnection
import cardetails as CarDetails
from facerecognition import FaceRecognition
import bluetoothlistener
# To consolidate logs into one location.
import logging
log = logging.getLogger(__name__)


class ValidateUser:
    """
    Validation entrypoint from the CLI. This can only be operated on when instantiated.
    This reduces unwarranted use of the validation function, and must be instantiated
    with the user's selection, and the class that contains the relevant data structurs.
    Without a valid selection, this will return False.
    """
    
    def __init__(self, userselection: int, current_car: CarDetails):
        self.userselection = userselection
        self.current_car = current_car
        log.info("Current Car object in init: {}".format(self.current_car))
        self.socket_connection = SocketConnection(self.current_car.get_car_id())

    def validateCredentials(self) -> bool:
        """
        This function is the entrypoint for any instantiation of this class.
        Solely for directing the user's choice to the appropriate function.
        Returns false if an invalid choice is made, otherwise returns
        true to indicate a return to the base state.
        """
        log.info("User Choice: {choice}".format(choice = self.userselection))
        if self.userselection == "1":
            self.validate_text()
            return True
        elif self.userselection == "2":
            self.validate_face()
            return True
        elif self.userselection == "9":
            self.validate_engineer()
            return True
        else:
            return False

    def validate_text(self):
        """
        Validates user's text credentials. Internally called. Returns after the number of attempts
        is exceeded or the user was true and the car has been returned.
        """

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
                print("Try again later.")
                time.sleep(3)
                return

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

    def validate_face(self):
        """
        Attempts to validate a face detection. Instantiates and calls the 
        :mod:`facerecognition` which accepts one parameter, the location of the 
        encodings file (pickle) and returns the token if the face is in the database
        for validation with the server.
        """
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
                return
            else:
                print("Booking not found.")
                time.sleep(3)
                return
        else:
            print("Face not recognised!\nPlease login with credentials.")
        time.sleep(2)
        return

    def validate_engineer(self):
        """
        This function is called when an engineer attempts to log in.
        It calls the appropriate bluetooth detection function in 
        the :mod:`bluetoothlistener` module and if an address is returned
        it then calls the socket connection and acts based on the return.
        """

        # Inform the user of the choice and action. Call bluetooth
        # detection function and act based on number of devices found.
        print("Validating engineer presence. \n \
        Please ensure your registered blueooth device is active....")
        btvalidation = bluetoothlistener.BluetoothListenerEngineer()
        detected_devices = btvalidation.catch_bluetooth()
        if len(detected_devices) > 0:
            # Devices were detected - determine if there is a valid
            # engineer booking at this car, acting appropriately
            # depending on the return.
            print("Validating device....")
            returned_dict = self.socket_connection.validate_engineer(detected_devices)
            log.info("returned_dict: {}".format(returned_dict))
            if returned_dict is None:
                print("Unable to establish server connection.")
                time.sleep(3)
                return
            if returned_dict is not False:
                self.current_car.engineer_access(returned_dict)
            else:
                print("No authorised devices detected. \n \
                Access denied!")
                time.sleep(3)
                return
        else:
            print("No devices found.")
            time.sleep(3)
            return


# For testing purposes.
if __name__ == "__main__":
    pass
    #main(sys.argv)
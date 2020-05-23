"""
Programming Internet of Things 2020 Semester 1
Assignment 2

This program controls the Agent Pi. 
It acts to verify a user by collecting either login details, or a
or a face recognition profile and sending this via a socket connection
to the Master Pi. Upon verification, the vehicle is unlocked, with
further options for locking the vehicle.

TODO use basic imagery on the sensehat to indicate the vehicle has
been unlocked or locked. This will further be used to indicate
when the device is attempting to image a face/QR code.

TODO it will broadcast bluetooth message to devices paired that 
listen in the appropriate manner.

TODO Catch any empty inputs in any of the forms. This could probably
be generalised into a utility call...? Depends on how it handles the 
empty string.
user_Input = input('Enter a string: ')
if not user_Input:
  print('Error: This field has not been filled out')
else:
  value = int(user_Input)
  print(value)
"""

# from datetime import datetime
import validation
# from validation import validateUser
from cardetails import CarDetails as CarDetails
from cardetails import CarLocationUpdater as CarLocationUpdater
import utilities
import os
import time
# import sys

# Could potentially move this to a module and then customise it a bit
# more if time is permitting.
import logging


# Car Identification for the car that this Agent Pi is lcoated in.
# This allows the CarID to be set elsewhere (for example in a json
# file).
class CarIDLoader:

    def __init__(self):
        this_car_id = str("")
        self.load_car_id()

    # Internal method for loading a card ID. Hides the method for determining 
    # the carID.
    def load_car_id(self):
        self.this_car_id = "car123"

    def get_car_id(self):
        return self.this_car_id


# # This class stores and can be used to update the location of the
# # car. It is designed to be instantiated by a CarDetails Object.
# # The location is stored as a dictionary and containes values
# # in Decimal Degrees, and the time that it was updated is also stored.
# class CarLocationUpdater:

#     def __init__(self, currentCarLocation: dict):
#         self.currentCarLocation = currentCarLocation

#     # Format the return value if necessary. Return the original values
#     # if the attempt to retrieve a locaiton fails.
#     def returnCarLocation(self):
#         retrievedLocation = self.updateCarLocation()
#         if retrievedLocation:
#             self.currentCarLocation["Longitude"] = retrievedLocation["Longitude"]
#             self.currentCarLocation["Latitude"] = retrievedLocation["Latitude"]
#             self.currentCarLocation["Time"] = datetime.now()
#         return self.currentCarLocation

#     # Internal method.
#     # Attempts to update the location, with a catch for all exceptions
#     # returning false. More detailed exception information should
#     # be handled by the function that actually determines the location.
#     # This should return a dictionary object that includes long/lat.
#     def updateCarLocation(self):
#         try:
#             # TODO For testing this will in future return a random location.
#             pass
#         except:
#             print("Error retrieving location data.")
#             return False


# # Contains and operates on the details regarding a car.
# class CarDetails:

#     # Beyond the obvious, this sets the location of the car at 0.0, 
#     # so it is is necessary when instantiating this object to call
#     # the updateLocation method if you want to use the actual
#     # location of the vehicle, but this will increase startup time.
#     def __init__(self, carID: str):
#         self.carID = carID
#         # Potentially store the last location in a file.
#         self.carLocation = {
#             "Longitude" : 0.0,
#             "Latitude" : 0.0,
#             "Time" : datetime.now()
#         }
#         self.carLocked = True
#         self.currentUser = None
    
#      # Returns the ID for passing onto Master Pi to validate booking.
#     def getCarID(self) -> str:
#         return self.carID

#     # Returns the last location of the vehicle as a Dictionary for passing
#     # onto Master Pi to terminate booking.
#     # Call update location first if you want the most up to date location
#     def getCarLocation(self) -> dict:
#         return self.carLocation

#     # Returns the current user of the vehicle, None if there is not a user.
#     def getCarUser(self) -> str:
#         return self.currentUser


#     def removeUser(self):
#         self.currentUser = None
#         self.carLocked = False

#     def unlock_car(self, newuser: str):
#         self.currentUser = newuser
#         self.carLocked = True

#     # Updates the current location of the car. This instantiates the
#     # CarLocationUpdater and attempts to update the location - there
#     # are two levels of error handling here, in case the CarLocationUpdater
#     # fails to return valid data, at which point it defaults to the previous
#     # known location.
#     def updateCarLocation(self):
#         locationUpdater = CarLocationUpdater(self.carLocation)
#         newLocation = locationUpdater.returnCarLocation()
#         # Attempt to update the location - if this fails due to key errors, 
#         # return values to original, notify, else fail hard and fast.
#         if "Longitude" in newLocation and \
#             "Latitude" in newLocation and \
#             "Time" in newLocation:
#             oldLocation = self.carLocation
#             try:
#                 self.carLocation["Longitude"] = newLocation["Longitude"]
#                 self.carLocation["Latitude"] = newLocation["Latitude"]
#                 self.carLocation["Time"] = newLocation["Time"]
#             except KeyError:
#                 self.carLocation = oldLocation
#                 print("Key assignment error - location data corrupt.")
#         else:
#             print("Required key in returned location data is missing.")


# The main controller - control is passed from the Main to this class
# when it is instantiated, and this class is where most user interactions occur.
# Essentially control stays here until the program exits.
class CLIController:

    def __init__(self, loaded_car: CarDetails):
        self.currentCar = loaded_car
        self.running = True
        # might be better to encrypt this info...?
        # the encryption could probably be used to login, so
        # as long as this data is not accessible, then it's probably okay...

    # This is the primary mechanim for user interactions to be responded to.
    # If a user successfully logs in, the appropriate details are stored ...
    # TODO only for a faceID datum to be added to their profile.
    # As such, the user_details dictionary only stores the minimum data required,
    # and removes this information if no longer needed.
    def activated(self):
        # These variable are stored inside the function to reduce visibility.
        # They will be completely integrated if an option to add face recognition
        # to a profile is offered.

        # TODO Deprecate this dictionary, as it should be contained in 
        # the validation module
        user_details = {
            "username": str(""),
            "password": str(""),
            "faceID": None}
        while self.running:
            # if self.loaded_car.carLocked:
            #     print("Welcome to Car Share System.\n")
            #     print("You are at Car ID: {car}\n\
            #     ".format(car = self.loaded_car.getCarID()))
            #     print("Please choose from the following options:\n \
            #           1. Unlock vehicle with username and password. \n \
            #           2. Unlock vehicle with face recognition. \n")
            #     user_choice = input("Please enter your selection as an integer: ")
            #     # pass the result to the Validation module that validates the credentials.
            #     # the username is returned, or False if invalid.
            #     # username = False
            #     # if user_choice == "1" or user_choice == "2":
            #     #     validateattempt = validation.validateUser(user_choice)
            #     validateattempt = validation.validateUser(user_choice)
            #     #else:
            #     if !validateattempt:
            #         # Invalid choice - pause, clear screen, flush keyboard input.
            #         print("Invalid Choice!")
            #         time.sleep(3)
            #         try:
            #             clearutil = utilities.helperUtilities()
            #             clearutil.clear_keyboard(sys.stdin)
            #         except:
            #             print("Clear keyboard operation not supported in debugger or this OS.")
            #             print("Exiting Program")
            #             sys.exit(0)
            #         os.system("clear")
            #         continue
            #     # IF the credentials are validated, the car is unlocked.
            #     if username:
            #         self.loaded_car.carLocked = False
            #     else:
            #         print("Invalid Credentials!")
            #         time.sleep(3)
            # else:
            #     print("Welcome {user} - have a safe journey.\n\
            #     ".format(user = self.user_details["username"]))

            os.system("clear")

            print("Welcome to Car Share System.\n")
            print("You are at Car ID: {car}\n\
            ".format(car=self.currentCar.get_car_id()))
            print("Please choose from the following options:\n \
                1. Unlock vehicle with username and password. \n \
                2. Unlock vehicle with face recognition. \n")
            user_choice = input("Please enter your selection as an integer: ")
            # pass the result to the Validation module that validates the credentials.
            # True is returned if the user was successful, and only after the
            # booking has been completed. False is immediately returned if invalid.
            # username = False
            # if user_choice == "1" or user_choice == "2":
            #     validateattempt = validation.ValidateUser(user_choice)
            user_validation = validation.ValidateUser(user_choice, self.currentCar)
            isvalid = user_validation.validateCredentials()

            if not isvalid:
                # Invalid choice - pause, clear screen, flush keyboard input.
                print("Invalid Choice!")
                time.sleep(3)
                clear_util = utilities.HelperUtilities()
                clear_util.clear_keyboard()

                # try:
                #     clearutil = utilities.helperUtilities()
                #     clearutil.clear_keyboard()
                # except:
                #     print("Clear keyboard operation not supported in debugger or this OS.")
                #     print("Exiting Program")
                #     sys.exit(0)
                # TODO is this continue needed?
                # continue

                      
                        

# Main class for starting the Agent Pi Software.
class Main():
    def start(self):
        # Begin the logging - change to rewrite if ongoing problems.
        logging.basicConfig(
            level = logging.DEBUG,
            filename = "operation_log.log", 
            filemode = "w", 
            format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s %(stack_info)s",
            datefmt = "%Y-%m-%d %H-%M-%S"
            )

        # Guide to implemented logging levels:
        # logging.debug("This is a debug message")
        # logging.info("This is an info message")
        # logging.warning("This is a warning message")
        # logging.error("This is an error message")
        # logging.critical("This is a critical message")
        # also:
        # logging.exception("An exception happened")

        # Can call the exception information withexc_info = True:
        # logging.error("blah exception", exc_info = True)
        # Alternatively call the exception function:
        # logging.exception() # which is a logging.error() level log
        # exception errors include the traceback information.

        # Load the CarID and then create a Car Object for operating on,
        # update the ID, remove the CardIDLoader to save memory.
        car_id_loader = CarIDLoader()
        current_car = CarDetails(car_id_loader.get_car_id())
        del car_id_loader

        # Update the location on loading...?
        # TODO this might not be necessary....
        current_car.update_car_location()

        # Pass the car details to the CLIGenerators and enable 
        # the user interaction via the CLI
        user_control = CLIController(current_car)
        user_control.activated()


AgentPi = Main()
AgentPi.start()

"""
Main module for the agent. This and the dependencies are called on to
manage the access to a vehicle. The program can be operated by executing 
this module. 
"""
# Programming Internet of Things 2020 Semester 1
# Assignment 2
# Cameron Bolton
# Jiewen Guan

# This and all modules contained therein contain multiple elements
# that are based on code procided as part of RMIT's Programming
# Intrnet of Things 2020 Semester 1 Course, and all references
# contained in those documents should be considered as sub-references.

# This program controls the Agent Pi. 
# It acts to verify a user by collecting either login details, or a
# or a face recognition profile and sending this via a socket connection
# to the Master Pi. Upon verification, the vehicle is unlocked, with
# further options for locking the vehicle.

# TODO use basic imagery on the sensehat to indicate the vehicle has
# been unlocked or locked. This will further be used to indicate
# when the device is attempting to image a face/QR code.

# TODO Catch any empty inputs in any of the forms. This could probably
# be generalised into a utility call...? Depends on how it handles the 
# empty string.


import os
import time
# This may be moved to an external log module and is subject to deprecation.
import logging

import validation
# from cardetails import CarDetails as CarDetails
# from cardetails import CarLocationUpdater as CarLocationUpdater
import cardetails
import utilities


# Car Identification for the car that this Agent Pi is lcoated in.
# This allows the CarID to be set elsewhere (for example in a json
# file).
class CarIDLoader:
    """
    This class is responsible for handling any details about the car
    while it is in an locked state, basically for performing any car
    related functions when the software is loaded.
    It is instantiated with nothing, and has one a primary function that
    returns a car_id.
    """

    def __init__(self):
        this_car_id = str("")
        self.load_car_id()

    def load_car_id(self):
        """
        Function for loading a car_id. Hides the process for 
        determining the car_id, and is called when instantiated.
        """
        self.this_car_id = "testcarX"

    def get_car_id(self):
        """
        Function for returning the car_id. This is typically called on when
        a booking is validated.
        """
        return self.this_car_id


class CLIController:
    """
    The main controller - control is passed from the Main to this class
    when it is instantiated, and this class is where most user interactions occur.
    Essentially control stays here until the program exits.
    It is responsible for displaying a CLI for the user. 
    It accepts a CarDetails object which should have details
    relative to the version loaded (at least the car_id) and 
    returns nothing.
    The sole method activated is called with no parameters.
    """

    def __init__(self, loaded_car: cardetails.CarDetails):
        self.currentCar = loaded_car
        self.running = True
        # might be better to encrypt this info...?
        # the encryption could probably be used to login, so
        # as long as this data is not accessible, then it's probably okay...

    # If a user successfully logs in, the appropriate details are stored ...
    # TODO only for a faceID datum to be added to their profile.
    # As such, the user_details dictionary only stores the minimum data required,
    # and removes this information if no longer needed.
    def activated(self):
        """
        Function that presents the user interface. It is the 
        primary mechanim for user interactions to be responded to.
        If a user is validated, the appropriate class is instantiated
        and control passed to it.
        Also provides access to engineers via hidden option 9 for 
        access via bluetooth detection.
        """
        while self.running:

            os.system("clear")

            print("Welcome to Car Share System.\n")
            print("You are at Car ID: {car}\n\
            ".format(car=self.currentCar.get_car_id()))
            print("Please choose from the following options:\n \
                1. Unlock vehicle with username and password. \n \
                2. Unlock vehicle with face recognition. \n")
            # 9. Engineer Access (hidden option)
            user_choice = input("Please enter your selection as an integer: ")
            # pass the result to the Validation module that validates the credentials.
            # True is returned if the user was successful, and only after the
            # booking has been completed. False is immediately returned if invalid.
            user_validation = validation.ValidateUser(user_choice, self.currentCar)
            isvalid = user_validation.validateCredentials()

            if not isvalid:
                # Invalid choice - pause, clear screen, flush keyboard input.
                print("Invalid Choice!")
                time.sleep(3)
                clear_util = utilities.HelperUtilities()
                clear_util.clear_keyboard()
                    
                        
class Main():
    """
    Main class that contains a single function that 
    when instantiated and called respectively, works 
    to load any neccessary details regarding the vehicle before 
    instantiateing the user interface with a call to :mod:'validation'
    """

    def start(self):
        """
        Primarily modification of this function will be regarding
        the level of logging to record, and whether this should 
        be a new file each time.
        """
        # Begin the logging - change to rewrite if ongoing problems.
        # Can also create a filename based on the start date of the program.
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
        current_car = cardetails.CarDetails(car_id_loader.get_car_id())
        del car_id_loader

        # Update the location on loading.
        current_car.update_car_location()

        # Pass the car details to the CLIGenerators and enable 
        # the user interaction via the CLI
        user_control = CLIController(current_car)
        user_control.activated()


if __name__ == "__main__":
    AgentPi = Main()
    AgentPi.start()

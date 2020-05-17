# This module contains the functionality that a user is offered when a
# car is unlocked.

import os

# The main class is constructed with the dictionary that was returned
# by the socket connection from the master pi. It has a single entry point
# of unlock_car that acts based on the dictionary that the class was 
# instantiated with.
class UnlockedCar():
    def __init__(self, unlocked_car: dict):
        self.unlocked_car = unlocked_car

    # Perform functions for unlocking the car.
    def unlock_car(self):
        # perform various unlock functions.


        # GUI Loop.
        in_booking = True
        while in_booking:
            print("Welcome {}".format(self.unlocked_car["username"]))
            print("Please select from the following options:\n \
            1. Return the Car.")
            user_choice = input("Enter your choice: ")

            if user_choice == "1":
                # TODO return the car via the MasterPi.
                in_booking = False
            elif user_choice == "9":
                # Update the uesr's face: prompt for a password, then 
                # call the updater.
                pass
            os.system("clear")
        return
    
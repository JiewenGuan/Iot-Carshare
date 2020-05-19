from datetime import datetime
import utilities
import os
import time
import sys
from unlockedcar import UnlockedCar as UnlockedCar

# To consolidate logs into one location.
import logging
log = logging.getLogger(__name__)

# Contains and operates on the details regarding a car.
class CarDetails:

    # Beyond the obvious, this sets the location of the car at 0.0, 
    # so it is is necessary when instantiating this object to call
    # the updateLocation method if you want to use the actual
    # location of the vehicle, but this will increase startup time.
    def __init__(self, car_id: str):
        self.car_id = car_id
        # Potentially store the last location in a file.
        self.carlocation = {
            "Longitude" : 0.0,
            "Latitude" : 0.0,
            "Time" : datetime.now()
        }
        self.carlocked = True
        self.currentuser = None
    
     # Returns the ID for passing onto Master Pi to validate booking.
    def get_car_id(self) -> str:
        return self.car_id

    # Returns the last location of the vehicle as a Dictionary for passing
    # onto Master Pi to terminate booking.
    # Call update location first if you want the most up to date location
    def getcarlocation(self) -> dict:
        return self.carlocation

    # Returns the current user of the vehicle, None if there is not a user.
    def get_car_user(self) -> str:
        return self.currentuser


    def remove_user(self):
        self.currentuser = None
        self.carlocked = False

    # def unlock_car(self, newuser: str):
    #     self.currentuser = newuser
    #     self.carlocked = True
    #     os.system("clear")
    #     print("Car Unlocked!")

    #     # GUI Loop.
    #     in_booking = True
    #     while in_booking:
    #         print("Welcome {}".format(self.get_car_user()))
    #         print("Please select from the following options:\n \
    #         1. Return the Car.")
    #         user_choice = input("Enter your choice: ")

    #         if user_choice == "1":
    #             # TODO return the car via the MasterPi.
    #             in_booking = False
    #         os.system("clear")

    #     # TODO do the things to return the car
    #     print("Car Returned.")
    #     time.sleep(3)

    def unlock_car(self, car_dict: dict):
        self.currentuser = car_dict["username"]
        self.carlocked = False
        os.system("clear")
        print("Car Unlocked!")
        time.sleep(1)
        unlocked_car = UnlockedCar(car_dict)
        unlocked_car.unlock_car()

        # TODO do the things to return the car
        print("Car Returned.")
        self.carlocked = True
        time.sleep(3)


    # Updates the current location of the car. This instantiates the
    # CarLocationUpdater and attempts to update the location - there
    # are two levels of error handling here, in case the CarLocationUpdater
    # fails to return valid data, at which point it defaults to the previous
    # known location.
    def update_car_location(self):
        location_updater = CarLocationUpdater(self.carlocation)
        new_location = location_updater.returncarlocation()
        # Attempt to update the location - if this fails due to key errors, 
        # return values to original, notify, else fail hard and fast.
        if "Longitude" in new_location and \
            "Latitude" in new_location and \
            "Time" in new_location:
            oldLocation = self.carlocation
            try:
                self.carlocation["Longitude"] = new_location["Longitude"]
                self.carlocation["Latitude"] = new_location["Latitude"]
                self.carlocation["Time"] = new_location["Time"]
            except KeyError:
                self.carlocation = oldLocation
                print("Key assignment error - location data corrupt.")
        else:
            print("Required key in returned location data is missing.")


# TODO this should really be called from the dar details, not by other functions...?

# This class stores and can be used to update the location of the
# car. It is designed to be instantiated by a CarDetails Object.
# The location is stored as a dictionary and containes values
# in Decimal Degrees, and the time that it was updated is also stored.
class CarLocationUpdater:

    def __init__(self, currentcar_location: dict):
        self.currentcar_location = currentcar_location

    # Format the return value if necessary. Return the original values
    # if the attempt to retrieve a locaiton fails.
    def returncarlocation(self):
        retrieved_location = self.update_car_location()
        if retrieved_location:
            self.currentcar_location["Longitude"] = retrieved_location["Longitude"]
            self.currentcar_location["Latitude"] = retrieved_location["Latitude"]
            self.currentcar_location["Time"] = datetime.now()
        return self.currentcar_location

    # Internal method.
    # Attempts to update the location, with a catch for all exceptions
    # returning false. More detailed exception information should
    # be handled by the function that actually determines the location.
    # This should return a dictionary object that includes long/lat.
    def update_car_location(self):
        try:
            # TODO For testing this will in future return a random location.
            pass
        except:
            print("Error retrieving location data.")
            return False
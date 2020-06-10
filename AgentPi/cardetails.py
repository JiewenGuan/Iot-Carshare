"""
The purpose of :mod:`cardetails` is to provide a separation of concerns
between an attempt to validate a user and their booking, the car in 
an unoccupied state, and this state - an occupied vehicle. As such it
acts to reduce the risk of data leaking.
"""
from datetime import datetime
import utilities
import os
import time
import sys

from unlockedcar import UnlockedCar as UnlockedCar
import engineeraccess
# To consolidate logs into one location.
import logging
log = logging.getLogger(__name__)


class CarDetails:
    """
    Contains and operates on the details regarding a car.
    Beyond the obvious, :class:`CarDetails` sets the location of the car at 0.0, 
    so it is is necessary when instantiating this object to call
    the updateLocation function if you want to use the actual
    location of the vehicle, but this will increase startup time.
    This class accepts the car_id upon instnatiation.
    """

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
    
    def get_car_id(self) -> str:
        """
        Returns the ID for passing onto Master Pi to validate booking.
        """
        return self.car_id


    def getcarlocation(self) -> dict:
        """
        Returns the last location of the vehicle as a Dictionary for passing
        onto Master Pi to terminate booking.
        Call :func:`update_car_location` location first if you want the most up to date location.
        """
        return self.carlocation

    def get_car_user(self) -> str:
        """
        Returns the current user of the vehicle, None if there is no a user.
        """
        return self.currentuser

    def remove_user(self):
        """
        Resets the car to an unoccupied state.
        """
        self.currentuser = None
        self.carlocked = False

    def unlock_car(self, car_dict: dict):
        """
        Called to unlock a car - accepts a dictionary of type retrieved from
        :mod:`agentdata`, which requires validated objects.
        """
        self.currentuser = car_dict["username"]
        self.carlocked = False
        os.system("clear")
        print("Car Unlocked!")
        time.sleep(1)
        unlocked_car = UnlockedCar(car_dict)
        unlocked_car.unlock_car()

        # If needed, perform other functioons things to return the car
        print("Car Returned.")
        self.carlocked = True
        time.sleep(3)

    def update_car_location(self):
        """
        Updates the current location of the car. This instantiates the
        CarLocationUpdater and attempts to update the location - there
        are two levels of error handling here, in case the CarLocationUpdater
        fails to return valid data, at which point it defaults to the previous
        known location.
        """
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

    def engineer_access(self, car_dict: dict):
        """
        Called when an engineer acccess the car.
        Presents a menu appropriate to an engineer once the car is unlocked.
        """

        # Store any appropriate data and pass control to the 
        # EngineerAccess class. 
        self.currentuser = car_dict["username"]
        self.carlocked = False
        os.system("clear")
        print("Access Granted.")
        time.sleep(1)
        engineer_access = engineeraccess.EngineerAccess(car_dict)
        engineer_access.unlock_car()

        print("Car Locked")
        self.carlocked = True
        time.sleep(3)
        return


class CarLocationUpdater:
    """
    This class stores and can be used to update the location of the
    car. It is designed to be instantiated by a CarDetails object.
    The location is stored as a dictionary and containes values
    in Decimal Degrees, and the time that it was updated is also stored.
    """
    def __init__(self, currentcar_location: dict):
        self.currentcar_location = currentcar_location

    def returncarlocation(self):
        """
        Format the return value if necessary. Return the original values
        if the attempt to retrieve a locaiton fails.
        """
        retrieved_location = self.update_car_location()
        if retrieved_location:
            self.currentcar_location["Longitude"] = retrieved_location["Longitude"]
            self.currentcar_location["Latitude"] = retrieved_location["Latitude"]
            self.currentcar_location["Time"] = datetime.now()
        return self.currentcar_location

    def update_car_location(self):
        """
        Internally called method.
        Attempts to update the location, with a catch for all exceptions
        returning false. More detailed exception information should
        be handled by the function that actually determines the location.
        This should return a dictionary object that includes long/lat.
        """
        try:
            # TODO For testing this will in future return a random location.
            pass
        except:
            print("Error retrieving location data.")
            return False

if __name__ == "__main__":
    pass
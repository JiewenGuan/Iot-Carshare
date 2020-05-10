from datetime import datetime
import utilities
import os
import time
import sys

# Contains and operates on the details regarding a car.
class CarDetails:

    # Beyond the obvious, this sets the location of the car at 0.0, 
    # so it is is necessary when instantiating this object to call
    # the updateLocation method if you want to use the actual
    # location of the vehicle, but this will increase startup time.
    def __init__(self, carID: str):
        self.carID = carID
        # Potentially store the last location in a file.
        self.carLocation = {
            "Longitude" : 0.0,
            "Latitude" : 0.0,
            "Time" : datetime.now()
        }
        self.carLocked = True
        self.currentUser = None
    
     # Returns the ID for passing onto Master Pi to validate booking.
    def getCarID(self) -> str:
        return self.carID

    # Returns the last location of the vehicle as a Dictionary for passing
    # onto Master Pi to terminate booking.
    # Call update location first if you want the most up to date location
    def getCarLocation(self) -> dict:
        return self.carLocation

    # Returns the current user of the vehicle, None if there is not a user.
    def getCarUser(self) -> str:
        return self.currentUser


    def removeUser(self):
        self.currentUser = None
        self.carLocked = False

    def unlock_car(self, newuser: str):
        self.currentUser = newuser
        self.carLocked = True

    # Updates the current location of the car. This instantiates the
    # CarLocationUpdater and attempts to update the location - there
    # are two levels of error handling here, in case the CarLocationUpdater
    # fails to return valid data, at which point it defaults to the previous
    # known location.
    def updateCarLocation(self):
        locationUpdater = CarLocationUpdater(self.carLocation)
        newLocation = locationUpdater.returnCarLocation()
        # Attempt to update the location - if this fails due to key errors, 
        # return values to original, notify, else fail hard and fast.
        if "Longitude" in newLocation and \
            "Latitude" in newLocation and \
            "Time" in newLocation:
            oldLocation = self.carLocation
            try:
                self.carLocation["Longitude"] = newLocation["Longitude"]
                self.carLocation["Latitude"] = newLocation["Latitude"]
                self.carLocation["Time"] = newLocation["Time"]
            except KeyError:
                self.carLocation = oldLocation
                print("Key assignment error - location data corrupt.")
        else:
            print("Required key in returned location data is missing.")


# TODO this should really be called from the dar details, not by other functions...?

# This class stores and can be used to update the location of the
# car. It is designed to be instantiated by a CarDetails Object.
# The location is stored as a dictionary and containes values
# in Decimal Degrees, and the time that it was updated is also stored.
class CarLocationUpdater:

    def __init__(self, currentCarLocation: dict):
        self.currentCarLocation = currentCarLocation

    # Format the return value if necessary. Return the original values
    # if the attempt to retrieve a locaiton fails.
    def returnCarLocation(self):
        retrievedLocation = self.updateCarLocation()
        if retrievedLocation:
            self.currentCarLocation["Longitude"] = retrievedLocation["Longitude"]
            self.currentCarLocation["Latitude"] = retrievedLocation["Latitude"]
            self.currentCarLocation["Time"] = datetime.now()
        return self.currentCarLocation

    # Internal method.
    # Attempts to update the location, with a catch for all exceptions
    # returning false. More detailed exception information should
    # be handled by the function that actually determines the location.
    # This should return a dictionary object that includes long/lat.
    def updateCarLocation(self):
        try:
            # TODO For testing this will in future return a random location.
            pass
        except:
            print("Error retrieving location data.")
            return False
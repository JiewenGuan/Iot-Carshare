"""
Module containing class(se) of helper utility functions.
"""
import select
import sys
import random
import time

# To consolidate logs into one location.
import logging
log = logging.getLogger(__name__)

class HelperUtilities:
    """
    Contains:
    - Function for clearing the input on unix systems.
    - Function for returning a GPS location.
    """

    def clear_keyboard(self):
        """
        Helper function to clear the keyboard after a sleep event. 
        it consumes each line until none remain, and then returns control to
        the calling function
        This may not function on windows - see https://docs.python.org/3/library/select.html
        and will throw an exception and exit as this is designed to run on raspbian raspberry pi.
        """
        try: 
            input_text = sys.stdin
            while input_text in select.select([input_text], [], [], 0)[0]:
                input_text.readline()
        except e:
            # Fourth paramter is timeout - set to zero to remove delay.
            print("Clear keyboard operation not supported in debugger or this OS.")
            log.exception(e)
            print("Exiting Program")
            time.sleep(3)
            sys.exit(0)

    def get_location(self):
        """
        A utility function that returns a random but real location.
        """
        location = [
            [-37.806995, 144.967241], 
            [-37.808955, 144.961880], 
            [-37.771171, 144.958180],
            [-37.676571, 145.070656],
            [-37.681663, 145.063820],
            [-37.839986, 144.927278],
            [-37.866852, 144.891067],
            [-37.780772, 144.914893],
            [-37.785501, 144.953378],
            [-37.831744, 144.892994]
            ]
        return random.choice(location)

# For testing.
if __name__ == "__main__":
    hu = HelperUtilities()
    print(hu.get_location())
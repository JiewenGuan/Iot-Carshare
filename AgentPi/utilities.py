import select
import sys
import random

# Class containing helper utilities.
class helperUtilities:
    # Helper function to clear the keyboard after a sleep event. 
    # it consumes each line until none remain, and then returns control to
    # the calling function
    def clear_keyboard(self):
        # This may not function on windows, - see https://docs.python.org/3/library/select.html
        # Fourth paramter is timeout - set to zero to remove delay.
        try: 
            input_text = sys.stdin
            while input_text in select.select([input_text], [], [], 0)[0]:
                input_text.readline()
        except e:
            print("Clear keyboard operation not supported in debugger or this OS.")
            print(e)
            print("Exiting Program")
            sys.exit(0)

    def get_location(self):
        location = [
            (-37.806995, 144.967241), 
            (-37.808955, 144.961880), 
            (-37.771171, 144.958180),
            (-37.676571, 145.070656),
            (-37.681663, 145.063820),
            (-37.839986, 144.927278),
            (-37.866852, 144.891067),
            (-37.780772, 144.914893),
            (-37.785501, 144.953378),
            (-37.831744, 144.892994)
            ]
        return random.choice(location)

    # A utility to clear the screen
    # TODO move this to a more appropriate place.
    # If this is implemented to deal with the cls command vs clear command in different OS.

if __name__ == "__main__":
    hu = helperUtilities()
    print(hu.get_location())
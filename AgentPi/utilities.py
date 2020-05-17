import select
import sys

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

    # A utility to clear the screen
    # TODO move this to a more appropriate place.
    # If this is implemented to deal with the cls command vs clear command in different OS.
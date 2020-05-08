import select
import sys

# Class containing helper utilities.
class helperUtilities:
    # Helper function to clear the keyboard after a sleep event.
    def clear_keyboard(self, input_text):
        # This may not function on windows, - see https://docs.python.org/3/library/select.html
        # Fourth paramter is timeout - set to zero to remove delay.
        while input_text in select.select([input_text], [], [], 0)[0]:
            input_text.readline()

    # A utility to clear the screen
    # TODO move this to a more appropriate place.
    # If this is implemented to deal with the cls command vs clear command in different OS.
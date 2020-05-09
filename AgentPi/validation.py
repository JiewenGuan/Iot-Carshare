# This class is responsible for accepting a user verification/validation
# choice, and then validating the user. If the user is validated, control
# is passed to a class that controls the vehicle (should this be the 
# intended action), else control is passed back to main.

from getpass import getpass
import sys

# Validation entrypoint. This can only be operated on when instantiated.
# This reduces unwarranted use of the validation function
class validateUser:
    
    # The init does the usual, but the userselection is the key as it 
    # assists the validatecredentials function in determining which
    # validate technique to use.
    def __init__(self, userselection: int, cardetails: dict):
        self.userselection = userselection
        self.currentCar = cardetails
        #self.validateCredentials()
        #print("is this executing?")

    # Solely for directing the users choice to the appropriate function.
    # Returns false if an invalid choice is made, otherwise returns
    # true to indicate a return to the base state.
    def validateCredentials(self) -> bool:
        #print("User Choice: {choice}".format(choice = self.userselection))
        if self.userselection == "1":
            self.validateText()
            return True
        elif self.userselection == "2":
            self.validateFace()
            return True
        else:
            return False

    # Validates user's text credentials. Returns after the number of attempts
    # is exceeded or the user was true and the car has been returned..
    def validateText(self):
        attempts = 3
        isvaliduser = False
        while attempts > 0:
            username = input("\nPlease enter your username: ")
            
            password = getpass()

            # Call validation function - validation function should return a boolean
            # then the boolean can be used to action the unlock functions.
            # eventually the boolean is returned 
            print("Validating credentials....")
            #TODO test whether it is necessary to clear the keyboard input....
            isvaliduser = False

            if isvaliduser:
                cardetails.updateUser(username)
                # Action unlock. From here all actions during a booking should take
                # place in and throughout this function call.
                # Return to the main menu. (cascades back through calling functions)
                break
            
            # decrement attempts and inform the user.
            attempts = attempts - 1
            print ("Credentials invalid for this car at this time!\n\
            Attempts remaining: {remains}".format(remains = attempts))

            

            

        


    # Validates a face detection.
    def validateFace(self):
        pass

if __name__ == "__main__":

    pass
    #main(sys.argv)


# Validation entrypoint. This can only be operated on when instantiated.
# This reduces unwarranted use of the validation function
class validateUser:
    # The init does the usual, but the userselection is the key as it 
    # assists the validatecredentials function in determining which
    # validate technique to use.
    def __init__(self, userselection: int):
        self.userselection = userselection
        self.validateCredentials()

    def validateCredentials(self):
        print("User Choice: {choice}".format(choice = self.userselection))


# Validates user credentials.
class validateText:
    pass


# Validates a face detection.
class validateFace:
    pass
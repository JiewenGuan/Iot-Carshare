# This module contains the classes that are used to
# communicate with the master pi.


# might be appropriate to move these classes into one class and call the function.

# Validate the text credentials 
class confirmText:
    def accept_credentials(self, username: str, password: str, car_id: str) -> bool:
        # This function will send the username, password, car_id and the current time to
        # the server for validation.


        # For testing only. In reality the username is returned from the server as 
        # confirmation that a booking is valid at the time.
        if username == password:
            return True
        return False



# Validate the face recognition.
class confirmFace:
    pass


# class for updating the Master Pi when the booking has been concluded
class updateMaster:
    pass



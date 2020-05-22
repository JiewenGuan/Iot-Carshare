# This module contains a single class provides the functionality for 
# acting on an agent dictionary. It accepts a dictionary and returns
# a modified dictionary when the apprpriate function is called, with 
# the same keys. 

import datetime

class MasterResponder():

    # Initialisation must include a dictionary.
    def __init__(self, agent_dictionary: dict):
        self.agent_dictionary = agent_dictionary
    
    # Called to validate username/password credentials.
    def validate_credentials(self) -> dict:
        # TODO Perform credential validation here
        valid_credentials = False

        # TODO Testing - update with actual validation call.
        if self.agent_dictionary["username"] == "uname":
            if self.agent_dictionary["password"] == "pword":
                if self.agent_dictionary["car_id"] == "car123":
                    valid_credentials = True
        
        self.update_return_dict(valid_credentials, self.agent_dictionary["username"])
        return self.agent_dictionary

    # Called to validate a face recognition token - must return a dictionary
    # with a username.
    def validate_face(self) -> dict:
        # TODO Perform face token validation here - this needs to return a username
        valid_credentials = False

        # TODO Testing - update with actual validation call.
        if self.agent_dictionary["usertoken"] == "abc123":
                if self.agent_dictionary["car_id"] == "car123":
                    username = "uname"
                    validate_credentials = True

        self.update_return_dict(valid_credentials, username)
        return self.agent_dictionary
    
    # Called to update the user's face recognition token
    def update_fr_token(self) -> dict:
        # TODO validate the password and username,
        # then update the face recognition token.
        token_update_success = False

        # TODO Testing - update with actual validation call.
        if self.agent_dictionary["username"] == self.agent_dictionary["password"]:
            token_update_success = True

        self.update_return_dict(token_update_success, self.agent_dictionary["username"])
        return self.agent_dictionary


    # Called to return the vehicle - returns just the car ID
    def return_vehicle(self) -> dict:
        # TODO Perform return functions HERE

        # clear dict and return it with the car_id
        temp_car_id = self.agent_dictionary["car_id"]
        self.clear_dict()
        self.agent_dictionary["car_id"] = temp_car_id
        return self.agent_dictionary

    # Helper to clear the dictionary.
    def clear_dict(self):
        for dict_keys in self.agent_dictionary:
            self.agent_dictionary[dict_keys] = None

    # Helper function to return a validated dictionary in the event
    # of a valid begin booking request.
    def update_return_dict(self, is_valid: bool, username: str):

        # Update the dictionary to conform with return requirements.
        if is_valid:
            self.agent_dictionary["password"] = None
            self.agent_dictionary["username"] = username
            self.agent_dictionary["usertoken"] = None
            self.agent_dictionary["action"] = None
            print ("Validated Dictionary: {}".format(self.agent_dictionary))
            # Set other dictionary elements
            # TODO return the end date of the hire?
        else:
            # Reset the dictionary to return it as empty
            self.clear_dict()
            self.agent_dictionary["info_date_time"] = datetime.datetime.now()
            print ("Cleared Dictionary: {}".format(self.agent_dictionary))
        # Convert the date and return
        self.agent_dictionary["info_date_time"] = self.agent_dictionary["info_date_time"].isoformat()






        # "action": self.action,
        # self.car_id = car_id
        # self.username = username
        # self.password = password
        # self.usertoken = usertoken
        # self.info_date_time = info_date_time
        # self.current_location = current_location



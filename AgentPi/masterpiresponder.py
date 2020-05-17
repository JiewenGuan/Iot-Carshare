# This module contains a single class provides the functionality for 
# acting on an agent dictionary. It accepts a dictionary and returns
# a modified dictionary when the apprpriate function is called, with 
# the same keys. 


class MasterResponder():

    def __init__(self, agent_dictionary: dict):
        self.agent_dictionary = agent_dictionary
    
    def validate_credentials(self) -> dict:
        # Validate the password
        valid_credentials = False
        # TODO Testing 
        if self.agent_dictionary["username"] == self.agent_dictionary["password"]:
            valid_credentials = True
        
        # Update the dictionary to conform with return requirements.
        if valid_credentials:
            self.agent_dictionary["password"] = None
            print ("Validated Dictionary: {}".format(self.agent_dictionary))
            # Set other dictionary elements
            # TODO return the end date of the hire?
        else:
            # Reset the dictionary to return it as empty
            for dict_keys in self.agent_dictionary:
                self.agent_dictionary[dict_keys] = None
            print ("Cleared Dictionary: {}".format(self.agent_dictionary))
            return self.agent_dictionary
        # Convert the date and return
        self.agent_dictionary["info_date_time"] = self.agent_dictionary["info_date_time"].isoformat()
        return self.agent_dictionary






        # "action": self.action,
        # self.car_id = car_id
        # self.username = username
        # self.password = password
        # self.usertoken = usertoken
        # self.info_date_time = info_date_time
        # self.current_location = current_location



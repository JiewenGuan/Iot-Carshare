# This module contains a single class provides the functionality for 
# acting on an agent dictionary. It accepts a dictionary and returns
# a modified dictionary when the apprpriate function is called, with 
# the same keys. 

import datetime, requests

class MasterResponder():

    # Initialisation must include a dictionary.
    def __init__(self, agent_dictionary: dict):
        self.agent_dictionary = agent_dictionary
    
    # Called to validate username/password credentials.
    def validate_credentials(self) -> dict:
        # TODO Perform credential validation here
        valid_credentials = False
        carname = self.agent_dictionary["car_id"]
        username = self.agent_dictionary["username"]
        password = self.agent_dictionary["password"]

        data = {'username':username,'password':password}
        r = requests.post('http://192.168.1.109:10100/auth',json = data, verify=False)
        user = r.json() or {}

        r = requests.get('http://192.168.1.109:10100/cars/{}'.format(carname), verify=False)
        car = r.json() or {}
        if user and car:
            if 'id' in user and 'id' in car:
                r = requests.get('http://192.168.1.109:10100/user_bookings/{}'.format(user['id']), verify=False)
                bookings = r.json() or {} 
                for booking in bookings:
                    if booking['car_id'] == car['id'] and booking['status'] == 1:
                        valid_credentials = True

        # TODO Testing - update with actual validation call.
        #if self.agent_dictionary["car_id"] == "car123":
            #if self.agent_dictionary["username"] == "uname":
                #if self.agent_dictionary["password"] == "pword":
                    #valid_credentials = True
        
        self.update_return_dict(valid_credentials, self.agent_dictionary["username"])
        return self.agent_dictionary

    # Called to validate a face recognition token - must return a dictionary
    # with a username.
    def validate_face(self) -> dict:
        # TODO Perform face token validation here - this needs to return a username
        valid_credentials = False
        username = None

        carname = self.agent_dictionary["car_id"]
        facetoken = self.agent_dictionary["usertoken"]
        
        data = {'facetoken':facetoken}
        r = requests.post('http://192.168.1.109:10100/facetoken',json = data, verify=False)
        user = r.json() or {}
        r = requests.get('http://192.168.1.109:10100/cars/{}'.format(carname), verify=False)
        car = r.json() or {}
        if user and car:
            if 'id' in user and 'id' in car:
                r = requests.get('http://192.168.1.109:10100/user_bookings/{}'.format(user['id']), verify=False)
                bookings = r.json() or {} 
                for booking in bookings:
                    if booking['car_id'] == car['id'] and booking['status'] == 1:
                        valid_credentials = True
                        username = user['username']

        # TODO Testing - update with actual validation call.
        #if self.agent_dictionary["usertoken"] == "abc123":
            #if self.agent_dictionary["car_id"] == "car123":
                #print("got here...?")
                #username = "uname"
                #valid_credentials = True

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
        
        carname = self.agent_dictionary["car_id"]
        location = self.agent_dictionary["current_location"]
        r = requests.get('http://192.168.1.109:10100/cars/{}'.format(carname), verify=False)
        car = r.json() or {}
        if 'id' in car:
            r = requests.get('http://192.168.1.109:10100/car_bookings/{}'.format(car['id']), verify=False)
            bookings = r.json() or {} 
            for booking in bookings:
                if booking['car_id'] == car['id'] and booking['status'] == 1:
                    if datetime.datetime.fromisoformat(booking['timestart']) > datetime.datetime.now():
                        r = requests.get('http://192.168.1.109:10100/cancel_booking/{}'.format(booking['id']), verify=False)
                    else:
                        r = requests.get('http://192.168.1.109:10100/return_booking/{}/{}'.format(booking['id'], location), verify=False)

        # TODO Testing code
        temp_car_id = None
        temp_action = None
        if self.agent_dictionary["car_id"] == "car123":
            temp_car_id = self.agent_dictionary["car_id"]
            temp_action = self.agent_dictionary["action"]

        # clear dict and return it with the car_id and the action
        # which are considered a confirmation of return.
        self.clear_dict()
        self.agent_dictionary["car_id"] = temp_car_id
        self.agent_dictionary["action"] = temp_action
        return self.agent_dictionary
    
    def invalid_action(self) -> dict:
        self.clear_dict()
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



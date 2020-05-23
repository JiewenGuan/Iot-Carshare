# This module performs an array of unit tests across the platform.
# In general, all modules involving human interaction immediately pass the
# user input to a new module or class or function. This affords our testing
# suite the flexibility to simulate human interaction by mimicking the inputs by passing
# them in directly. It is not considered necessary to test the input() method
# itself, and user inputs lack complexity that warrants testing beyond
# user testing.
# It also includes integration tests - essentially this is a cascade of tests
# that begin by testing the data structures, then testing endpoints for data
# and migrating further from these end points. For example, first the dicionary
# creator class is tested (input validation, dictionary return validity, internal
# data modification methods), then a socket connection is validated, then a
# dictionary is sent via sockets with the return unvalidated, then the return
# is validated, and finally the simulations of user input which itself generated
# a dictionary which is then passed to the socket and validated by the server and 
# returned is validated.

import datetime
import unittest
import random

# Modules containing classes for unit testing of the agentpi.
# Note that not all classes are imported, as these classes import
# all the classes to be tested by consequence.
import agentdata
import utilities
import socketconnection


# Test utilities.py
class TestUtilities(unittest.TestCase):

    def setUp(self):
        # Create a location to test on.
        helper_utilities = utilities.HelperUtilities()
        self.location = helper_utilities.get_location()
        print("Test suite: {}".format(type(self).__name__))

    def test_utility_return_types(self):
        self.assertEqual(type(self.location), list)
        self.assertEqual(type(self.location[0]), float)
        self.assertEqual(type(self.location[1]), float)

    def test_utility_size(self):
        # Test the location return types.
        self.assertEqual(len(self.location), 2)

    def test_utility_location_edges(self):
        # Test edge cases.
        self.assertTrue(self.location[0] <= 90)
        self.assertTrue(self.location[0] >= -90)
        self.assertTrue(self.location[1] <= 180)
        self.assertTrue(self.location[1] >= -180)


# Test agentdata.py
# Do not use helper functions to create dictionary.
class TestAgentData(unittest.TestCase):

    def setUp(self):
        # Set Data to be converted.
        self.date_to_use = datetime.datetime.now()
        self.car_name = "car123"
        self.test_data = agentdata.DictionaryConstructor(self.car_name, self.date_to_use)
        self.action = 1
        self.username = "uname"
        self.password = "pword"
        self.usertoken = "abc123"
        self.test_data.set_action(1)
        self.test_data.set_username(self.username)
        self.test_data.set_password(self.password)
        self.test_data.set_usertoken(self.usertoken)
        # Call a location 
        helper_utilities = utilities.HelperUtilities()
        self.location = helper_utilities.get_location()
        self.test_data.set_current_location(self.location)
        print("Test suite: {}".format(type(self).__name__))

    def test_data_integrity(self):
        # Call the data to be returned.
        returned_data = self.test_data.get_socket_dictionary()
        self.assertEqual(returned_data["action"], self.action)
        self.assertEqual(returned_data["car_id"], self.car_name)
        self.assertEqual(returned_data["username"], self.username)
        self.assertEqual(returned_data["password"], self.password)
        self.assertEqual(returned_data["usertoken"], self.usertoken)
        self.assertEqual(returned_data["info_date_time"], self.date_to_use)
        self.assertEqual(returned_data["current_location"], self.location)

    def test_date_converter(self):
        # Tests the conversion of dates for JSON transport through sockets.
        returned_data = self.test_data.get_socket_dictionary()
        returned_iso_date = returned_data["info_date_time"]
        modified_date = datetime.datetime.isoformat(returned_iso_date)
        custom_modifier = agentdata.DictionaryDateUpdater(modified_date)
        returned_date = custom_modifier.get_python_date()
        self.assertEqual(returned_date, returned_iso_date)


# test socketconnection.py
# by implication tests socketresponder.py
# by implication tests masterpiresponder.pi
# Tests the raw socket.
class TestSocketConnection(unittest.TestCase):
    # Unit test user validation with credentials.

    # Having tested the dictionary creator, we need to create a dictionary
    # in the socketconnection.
    def setUp(self):
        self.test_data_true = dictionary_class_helper_true()
        self.test_data_false = dictionary_class_helper_false()
        self.sock_conn = socketconnection.SocketConnection(self.test_data_true.car_id)
        print("Test suite: {}".format(type(self).__name__))

    # Test the connection
    def test_socket_conn_true(self):
        dict_to_test_true = self.test_data_true.get_socket_dictionary()
        returned_dict = self.sock_conn.validation_returner(dict_to_test_true)
        self.assertTrue(returned_dict is not None)
        
    # Test the connection responds to invalid but correctly formatted data.
    def test_socket_conn_false(self):
        dict_to_test_false = self.test_data_false.get_socket_dictionary()
        returned_dict = self.sock_conn.validation_returner(dict_to_test_false)
        self.assertTrue(returned_dict is not None)


# test socketconnection.py
# As above by implication, but this tests the conditional return of the socket
# independent of validation on the AgentPi. 
# The purpose is to edge cases where a single value in the dictionary should
# determine the result of processing the entire dictionary.
# Essentially this ensures that only fully valid dictionaries will yield
# a positive response.
class TestSocketResponseAction1(unittest.TestCase):

    def setUp(self):
        self.test_data_true = dictionary_class_helper_true()
        self.test_data_false = dictionary_class_helper_false()
        self.sock_conn = socketconnection.SocketConnection(self.test_data_true.car_id)
        self.valid_dict = self.test_data_true.get_socket_dictionary()
        self.invalid_dict = self.test_data_false.get_socket_dictionary()
        print("Test suite: {}".format(type(self).__name__))

    # Test a dictionary that has all but one parameter correct.
    # These should return a dictionary with None, which is returned to the
    # test as False. i.e., invalid booking details.

    # Incorrect car_id
    def test_a1_invalid_car_id(self):
        test_dict = self.valid_dict
        test_dict["car_id"] = self.invalid_dict["car_id"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, False)

    # Incorrect username
    def test_a1_invalid_username(self):
        test_dict = self.valid_dict
        test_dict["username"] = self.invalid_dict["username"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, False)

    # Incorrect password
    def test_a1_invalid_password(self):
        test_dict = self.valid_dict
        test_dict["password"] = self.invalid_dict["password"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, False)

    # Incorret usertoken - this should return a valid dictionary.
    def test_a1_invalid_usertoken(self):
        test_dict = self.valid_dict
        test_dict["usertoken"] = self.invalid_dict["usertoken"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict["username"], test_dict["username"])

    # Incorrect date - will fail unless Master is connected to database.
    def test_a1_invalid_info_date_time(self):
        test_dict = self.valid_dict
        test_dict["info_date_time"] = self.invalid_dict["info_date_time"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, False)


# As above, but for action 2 (validating a face recognition)
class TestSocketResponseAction2(unittest.TestCase):

    # Test a dictionary that has all but one parameter correct.
    # These should return a dictionary with None, which is returned to the
    # test as False. i.e., invalid booking details.
    def setUp(self):
        self.test_data_true = dictionary_class_helper_true()
        self.test_data_true.set_action(2)
        self.test_data_false = dictionary_class_helper_false()
        self.sock_conn = socketconnection.SocketConnection(self.test_data_true.car_id)
        self.valid_dict = self.test_data_true.get_socket_dictionary()
        self.invalid_dict = self.test_data_false.get_socket_dictionary()
        print("Test suite: {}".format(type(self).__name__))

    # Incorrect car_id
    def test_a2_invalid_car_id(self):
        test_dict = self.valid_dict
        test_dict["car_id"] = self.invalid_dict["car_id"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, False)

    # Incorrect username - should return valid dictionary.
    def test_a2_invalid_username(self):
        test_dict = self.valid_dict
        test_dict["username"] = self.invalid_dict["username"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        # print("Username that should be valid: {}".format(self.valid_dict["username"]))
        self.assertEqual(returned_dict["username"], self.test_data_true.username)

    # Incorrect password - should return valid dictionary.
    def test_a2_invalid_password(self):
        test_dict = self.valid_dict
        test_dict["password"] = self.invalid_dict["password"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        # print("\nTest send: {}".format(test_dict))
        # print("Test return: {}\n".format(returned_dict))
        self.assertEqual(returned_dict["username"], self.valid_dict["username"])

    # Incorrect usertoken
    def test_a2_invalid_usertoken(self):
        test_dict = self.valid_dict
        test_dict["usertoken"] = self.invalid_dict["usertoken"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, False)

    # Incorrect date - will fail unless Master is connected to database.
    def test_a2_invalid_info_date_time(self):
        test_dict = self.valid_dict
        test_dict["info_date_time"] = self.invalid_dict["info_date_time"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, False)


# As above, but for action 4 (return a vehicle)
class TestSocketResponseAction4(unittest.TestCase):
    
    def setUp(self):
        self.test_data_true = dictionary_class_helper_true()
        self.test_data_true.set_action(4)
        self.test_data_false = dictionary_class_helper_false()
        self.sock_conn = socketconnection.SocketConnection(self.test_data_true.car_id)
        self.valid_dict = self.test_data_true.get_socket_dictionary()
        self.invalid_dict = self.test_data_false.get_socket_dictionary()
        print("Test suite: {}".format(type(self).__name__))

    # Incorrect car_id
    def test_a4_invalid_car_id(self):
        test_dict = self.valid_dict
        test_dict["car_id"] = self.invalid_dict["car_id"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, False)

    # Incorrect username.
    def test_a4_invalid_username(self):
        test_dict = self.valid_dict
        # reset the car_id
        test_dict["car_id"] = self.test_data_true.car_id
        test_dict["username"] = self.invalid_dict["username"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        # print("Username that should be valid: {}".format(self.valid_dict["username"]))
        self.assertEqual(returned_dict, True)

    # Incorrect password.
    def test_a4_invalid_password(self):
        test_dict = self.valid_dict
        # reset the car_id
        test_dict["car_id"] = self.test_data_true.car_id
        test_dict["password"] = self.invalid_dict["password"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        # print("\nTest send: {}".format(test_dict))
        # print("Test return: {}\n".format(returned_dict))
        self.assertEqual(returned_dict, True)

    # Incorrect usertoken.
    def test_a4_invalid_usertoken(self):
        test_dict = self.valid_dict
        # reset the car_id
        test_dict["car_id"] = self.test_data_true.car_id
        test_dict["usertoken"] = self.invalid_dict["usertoken"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, True)

    # Incorrect date.
    def test_a4_invalid_info_date_time(self):
        test_dict = self.valid_dict
        # reset the car_id
        test_dict["car_id"] = self.test_data_true.car_id
        test_dict["info_date_time"] = self.invalid_dict["info_date_time"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, True)


# socketconnection.py
# This tests the entry points of the validation methods.
# Essentially it interfaces directly with the functions
# that the user input is passed to. This checks for the 
# appropriate responses with the minimal data required.
class TestSocketValidation(unittest.TestCase):

    def setUp(self):
        self.test_data_true = dictionary_class_helper_true()
        self.test_data_false = dictionary_class_helper_false()
        self.sock_conn_valid = socketconnection.SocketConnection(self.test_data_true.car_id)
        self.sock_conn_invalid = socketconnection.SocketConnection(self.test_data_false.car_id)
        self.valid_dict = self.test_data_true.get_socket_dictionary()
        self.invalid_dict = self.test_data_false.get_socket_dictionary()
        print("Test suite: {}".format(type(self).__name__))

    # Test valid credential response
    def test_valid_cred(self):
        returned_dict = self.sock_conn_valid.validate_text_credentials(
            self.valid_dict["username"], 
            self.valid_dict["password"]
            )
        self.assertEqual(self.valid_dict["username"], returned_dict["username"])
        
    # Test invalid credential response
    def test_invalid_cred(self):
        returned_dict = self.sock_conn_valid.validate_text_credentials(
            self.invalid_dict["username"], 
            self.invalid_dict["password"]
            )
        self.assertEqual(returned_dict, False)

    
    # Test valid token response
    def test_valid_token(self):
        returned_dict = self.sock_conn_valid.validate_face_credentials(
            self.valid_dict["usertoken"] 
            )
        self.assertEqual(returned_dict["username"], self.valid_dict["username"])

    # Test invalid token response
    def test_invalid_token(self):
        returned_dict = self.sock_conn_valid.validate_face_credentials(
            self.invalid_dict["usertoken"] 
            )
        self.assertEqual(returned_dict, False)


    # Test invalid car but valid credentials
    def test_invalid_car_cred(self):
        returned_dict = self.sock_conn_invalid.validate_text_credentials(
            self.valid_dict["username"], 
            self.valid_dict["password"]
            )
        self.assertEqual(returned_dict, False)

    # Test invalid car but valid token
    def test_invalid_car_token(self):
        returned_dict = self.sock_conn_invalid.validate_face_credentials(
            self.valid_dict["usertoken"] 
            )
        self.assertEqual(returned_dict, False)


            # "action": self.action,
            # "car_id": self.car_id,
            # "username": self.username,
            # "password": self.password,
            # "usertoken": self.usertoken,
            # "info_date_time": self.info_date_time,
            # "current_location": self.current_location

# This class tests edge cases resulting in an invalid action
# Basically send a random integer as the action that is not one of the
# accepted actions and do this say 10 times....
class TestInvalidAction(unittest.TestCase):

    def setUp(self):
        self.test_data_true = dictionary_class_helper_true()
        self.test_data_false = dictionary_class_helper_false()
        self.sock_conn_valid = socketconnection.SocketConnection(self.test_data_true.car_id)
        self.valid_dict = self.test_data_true.get_socket_dictionary()
        print("Test suite: {}".format(type(self).__name__))

    # x = 0
    # while x < 10:
    def test_invalid_action(self):
        action = random.randint(-10000,10000)
        if action < 1 or action > 4:
            test_dict = self.valid_dict
            test_dict["action"] = action
            returned_dict = self.sock_conn_valid.validation_returner(test_dict)
            self.assertEqual(returned_dict, False)
            # x += 1

# These two helper functions return dictionary class objects for testing purposes.
# The only elements that do not change is the action.
# To build tests that look at each element of the object,
# Use the setters, changing the object by one element at time.
def dictionary_class_helper_true() -> agentdata.DictionaryConstructor:
    # Set Data to be converted.
    date_to_use = datetime.datetime.now().isoformat()
    car_name = "car123"
    test_data = agentdata.DictionaryConstructor(car_name, date_to_use)
    action = 1
    username = "uname"
    password = "pword"
    usertoken = "abc123"
    test_data.set_action(1)
    test_data.set_username(username)
    test_data.set_password(password)
    test_data.set_usertoken(usertoken)
    # Call a location 
    helper_utilities = utilities.HelperUtilities()
    location = helper_utilities.get_location()
    test_data.set_current_location(location)
    return test_data

def dictionary_class_helper_false() -> agentdata.DictionaryConstructor:
    # Set Data to be converted.
    date_to_use = (datetime.datetime.now() - datetime.timedelta(days=365)).isoformat()
    car_name = "fabc123"
    test_data = agentdata.DictionaryConstructor(car_name, date_to_use)
    action = 1
    username = "funame"
    password = "fpword"
    usertoken = "fabc123"
    test_data.set_action(1)
    test_data.set_username(username)
    test_data.set_password(password)
    test_data.set_usertoken(usertoken)
    # Call a location 
    helper_utilities = utilities.HelperUtilities()
    location = helper_utilities.get_location()
    test_data.set_current_location(location)
    return test_data

if __name__ == '__main__':
    unittest.main()
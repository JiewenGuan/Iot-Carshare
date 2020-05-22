# This module performs an array of unit tests across the platform.
import datetime
import unittest

# Modules containing classes for unit testing of the agentpi.
import agentdata
import utilities
import socketconnection

# Test utilities.py
class TestUtilities(unittest.TestCase):

    def setUp(self):
        # Create a location to test on.
        helper_utilities = utilities.HelperUtilities()
        self.location = helper_utilities.get_location()

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

    # Test the connection
    def test_socket_conn_true(self):
        dict_to_test_true = self.test_data_true.get_socket_dictionary()
        returned_dict = self.sock_conn.validation_returner(dict_to_test_true)
        self.assertTrue(returned_dict is not None)

    def test_socket_conn_false(self):
        dict_to_test_false = self.test_data_false.get_socket_dictionary()
        returned_dict = self.sock_conn.validation_returner(dict_to_test_false)
        self.assertTrue(returned_dict is not None)


# test socketconnection.py
# As above by implication, but this tests the entry points rather than the 
# raw socket.
class TestSocketValidation(unittest.TestCase):
    def setUp(self):
        self.test_data_true = dictionary_class_helper_true()
        self.test_data_false = dictionary_class_helper_false()
        self.sock_conn = socketconnection.SocketConnection(self.car_id)
    # Unit test user face with the token.

    # Test return a car.

# These two helper functions return dictionary class objects for testing purposes.
# The only elements that do not change is the action.
# To build tests that look at each element of the object,
# Use the setters, changing the object by one element at time.
def dictionary_class_helper_true() -> dict:
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

def dictionary_class_helper_false() -> dict:
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
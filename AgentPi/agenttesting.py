"""
This module performs an array of unit tests across the platform.
In general, all modules involving human interaction immediately pass the
user input to a new module or class or function. This affords our testing
suite the flexibility to simulate human interaction by mimicking the inputs by passing
them in directly. It is not considered necessary to test the input() method
itself, and user inputs lack complexity that warrants testing beyond
user testing.
It also includes integration tests - essentially this is a cascade of tests
that begin by testing the data structures, then testing endpoints for data
and migrating further from these end points. For example, first the dicionary
creator class is tested (input validation, dictionary return validity, internal
data modification methods), then a socket connection is validated, then a
dictionary is sent via sockets with the return unvalidated, then the return
is validated, and finally the simulations of user input which itself generated
a dictionary which is then passed to the socket and validated by the server and 
returned is validated.
"""

import datetime
import unittest
import random

# Modules containing classes for unit testing of the agentpi.
# Note that not all classes are imported, as these classes import
# all the classes to be tested by consequence.
import agentdata
import utilities
import socketconnection


class TestUtilities(unittest.TestCase):
    """
    Primary testing class for :mod:`utilities`
    """

    def setUp(self):
        """
        Create a location to test on.
        """
        helper_utilities = utilities.HelperUtilities()
        self.location = helper_utilities.get_location()
        print("Test suite: {}".format(type(self).__name__))

    def test_utility_return_types(self):
        """
        Validates the return types.
        """
        self.assertEqual(type(self.location), list)
        self.assertEqual(type(self.location[0]), float)
        self.assertEqual(type(self.location[1]), float)

    def test_utility_size(self):
        """
        Test the location return types.
        """
        self.assertEqual(len(self.location), 2)

    def test_utility_location_edges(self):
        """
        Test edge cases.
        """
        self.assertTrue(self.location[0] <= 90)
        self.assertTrue(self.location[0] >= -90)
        self.assertTrue(self.location[1] <= 180)
        self.assertTrue(self.location[1] >= -180)


class TestAgentData(unittest.TestCase):
    """
    This class tests the :mod:`agentdata` module.

    .. warning:: Do not use helper functions to create a dictionary.
    """

    def setUp(self):
        """
        Set Data to be converted and validated.
        """
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
        """
        Tests the data returned.
        """
        returned_data = self.test_data.get_socket_dictionary()
        self.assertEqual(returned_data["action"], self.action)
        self.assertEqual(returned_data["car_id"], self.car_name)
        self.assertEqual(returned_data["username"], self.username)
        self.assertEqual(returned_data["password"], self.password)
        self.assertEqual(returned_data["usertoken"], self.usertoken)
        self.assertEqual(returned_data["info_date_time"], self.date_to_use)
        self.assertEqual(returned_data["current_location"], self.location)

    def test_date_converter(self):
        """
        Tests the conversion of dates for JSON transport through sockets.
        """
        returned_data = self.test_data.get_socket_dictionary()
        returned_iso_date = returned_data["info_date_time"]
        modified_date = datetime.datetime.isoformat(returned_iso_date)
        custom_modifier = agentdata.DictionaryDateUpdater(modified_date)
        returned_date = custom_modifier.get_python_date()
        self.assertEqual(returned_date, returned_iso_date)


class TestSocketConnection(unittest.TestCase):
    """
    This class tests :mod:`socketconnection` and by implication,
    also tests :mod:`socketresponder` and :mod:`masterpiresponder`.
    As such, it tests the raw socket, and requires database interaction to pass.

    .. warning:: Some of these tests will FAIL if testing on the actual database
        unless the database is updated with the requisite bookings.

    .. note:: These tests will also fail, as will tests that refer to this class
        in the comments if :class:`TestAgentData` fails.
    """

    def setUp(self):
        """
        It is necessary to instantiate the true data class and extract the
        relevant dictionary.
        A valid socket connection is also required.
        """
        self.test_data_true = dictionary_class_helper_true()
        self.test_data_false = dictionary_class_helper_false()
        self.sock_conn = socketconnection.SocketConnection(self.test_data_true.car_id)
        print("Test suite: {}".format(type(self).__name__))

    def test_socket_conn_true(self):
        """
        Test the connection
        """
        dict_to_test_true = self.test_data_true.get_socket_dictionary()
        returned_dict = self.sock_conn.validation_returner(dict_to_test_true)
        self.assertTrue(returned_dict is not None)
      
    def test_socket_conn_false(self):
        """
        Test the connection responds to invalid but correctly formatted data.
        """
        dict_to_test_false = self.test_data_false.get_socket_dictionary()
        returned_dict = self.sock_conn.validation_returner(dict_to_test_false)
        self.assertTrue(returned_dict is not None)


class TestSocketResponseAction1(unittest.TestCase):
    """
    As in :class:`TestSocketConnection` by implication, but this tests the conditional 
    return of the socketindependent of validation on the AgentPi. 
    The purpose is to edge cases where a single value in the dictionary should
    determine the result of processing the entire dictionary.
    Essentially this ensures that only fully valid dictionaries will yield
    a positive response.
    Test a dictionary that has all but one parameter correct.
    These should return a dictionary with None, which is returned to the
    test as False. i.e., invalid booking details.
    """

    def setUp(self):
        """
        It is necessary to instantiate the data classes and extract the
        relevant dictionaries.
        It additionally requires a socket connection.
        """
        self.test_data_true = dictionary_class_helper_true()
        self.test_data_false = dictionary_class_helper_false()
        self.sock_conn = socketconnection.SocketConnection(self.test_data_true.car_id)
        self.valid_dict = self.test_data_true.get_socket_dictionary()
        self.invalid_dict = self.test_data_false.get_socket_dictionary()
        print("Test suite: {}".format(type(self).__name__))

    def test_a1_invalid_car_id(self):
        """
        Test an incorrect car_id
        """
        test_dict = self.valid_dict
        test_dict["car_id"] = self.invalid_dict["car_id"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, False)

    def test_a1_invalid_username(self):
        """
        Test an incorrect username
        """
        test_dict = self.valid_dict
        test_dict["username"] = self.invalid_dict["username"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, False)

    def test_a1_invalid_password(self):
        """
        Test an incorrect password
        """
        test_dict = self.valid_dict
        test_dict["password"] = self.invalid_dict["password"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, False)

    def test_a1_invalid_usertoken(self):
        """
        Test an incorrect usertoken - this should return a valid dictionary.
        """
        test_dict = self.valid_dict
        test_dict["usertoken"] = self.invalid_dict["usertoken"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        # self.assertEqual(returned_dict["username"], test_dict["username"])
        self.assertEqual(returned_dict, False)

    def test_a1_invalid_info_date_time(self):
        """
        Test an incorrect date - will fail unless Master is connected to database.
        """
        test_dict = self.valid_dict
        test_dict["info_date_time"] = self.invalid_dict["info_date_time"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, False)


class TestSocketResponseAction2(unittest.TestCase):
    """
    As :class:TestSocketResponseAction1`, but for action 2 (validating a face recognition)
    Test a dictionary that has all but one parameter correct.
    These should return a dictionary with None, which is returned to the
    test as False. i.e., invalid booking details.
    """

    def setUp(self):
        """
        It is necessary to instantiate the data classes and extract the
        relevant dictionaries.
        This test suite also requires a socket connection.
        """
        self.test_data_true = dictionary_class_helper_true()
        self.test_data_true.set_action(2)
        self.test_data_false = dictionary_class_helper_false()
        self.sock_conn = socketconnection.SocketConnection(self.test_data_true.car_id)
        self.valid_dict = self.test_data_true.get_socket_dictionary()
        self.invalid_dict = self.test_data_false.get_socket_dictionary()
        print("Test suite: {}".format(type(self).__name__))

    def test_a2_invalid_car_id(self):
        """
        Test an incorrect car_id
        """
        test_dict = self.valid_dict
        test_dict["car_id"] = self.invalid_dict["car_id"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, False)

    def test_a2_invalid_username(self):
        """
        Incorrect username - should return a valid dictionary that is empty or false.
        """
        test_dict = self.valid_dict
        test_dict["username"] = self.invalid_dict["username"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        # print("Username that should be valid: {}".format(self.valid_dict["username"]))
        # self.assertEqual(returned_dict["username"], self.test_data_true.username)
        self.assertEqual(returned_dict, False)
    def test_a2_invalid_password(self):
        """
        Incorrect password - should return a valid dictionary that is empty or false.
        """
        test_dict = self.valid_dict
        test_dict["password"] = self.invalid_dict["password"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        # print("\nTest send: {}".format(test_dict))
        # print("Test return: {}\n".format(returned_dict))
        # self.assertEqual(returned_dict["username"], self.valid_dict["username"])
        self.assertEqual(returned_dict, False)

    def test_a2_invalid_usertoken(self):
        """
        Tests an incorrect usertoken.
        """
        test_dict = self.valid_dict
        test_dict["usertoken"] = self.invalid_dict["usertoken"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, False)

    def test_a2_invalid_info_date_time(self):
        """
        Incorrect date - will fail unless Master is connected to database.
        """
        test_dict = self.valid_dict
        test_dict["info_date_time"] = self.invalid_dict["info_date_time"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, False)


class TestSocketResponseAction4(unittest.TestCase):
    """
    As in :class:`TestSocketResponseAction1`, but for action 4 (return a vehicle).
    """

    def setUp(self):
        """
        It is necessary to instantiate the data classes and extract the
        relevant dictionaries.
        This testing suite also requires a socket connection.
        """
        self.test_data_true = dictionary_class_helper_true()
        self.test_data_true.set_action(4)
        self.test_data_false = dictionary_class_helper_false()
        self.sock_conn = socketconnection.SocketConnection(self.test_data_true.car_id)
        self.valid_dict = self.test_data_true.get_socket_dictionary()
        self.invalid_dict = self.test_data_false.get_socket_dictionary()
        print("Test suite: {}".format(type(self).__name__))

    def test_a4_invalid_car_id(self):
        """
        Tests an incorrect car_id
        """
        test_dict = self.valid_dict
        test_dict["car_id"] = self.invalid_dict["car_id"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, False)

    def test_a4_invalid_username(self):
        """
        Tests an incorrect username
        """
        test_dict = self.valid_dict
        # reset the car_id
        test_dict["car_id"] = self.test_data_true.car_id
        test_dict["username"] = self.invalid_dict["username"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        # print("Username that should be valid: {}".format(self.valid_dict["username"]))
        self.assertEqual(returned_dict, True)

    def test_a4_invalid_password(self):
        """
        Tests an incorrect password
        """
        test_dict = self.valid_dict
        # reset the car_id
        test_dict["car_id"] = self.test_data_true.car_id
        test_dict["password"] = self.invalid_dict["password"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, True)

    def test_a4_invalid_usertoken(self):
        """
        Tests an incorrect usertoken.
        """
        test_dict = self.valid_dict
        # reset the car_id
        test_dict["car_id"] = self.test_data_true.car_id
        test_dict["usertoken"] = self.invalid_dict["usertoken"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, True)

    def test_a4_invalid_info_date_time(self):
        """
        Tests an incorrect date.
        """
        test_dict = self.valid_dict
        # reset the car_id
        test_dict["car_id"] = self.test_data_true.car_id
        test_dict["info_date_time"] = self.invalid_dict["info_date_time"]
        returned_dict = self.sock_conn.validation_returner(test_dict)
        self.assertEqual(returned_dict, True)


class TestSocketValidation(unittest.TestCase):
    """
    This tests the entry points of the validation methods of :mod:`socketconnection`.
    Essentially it interfaces directly with the functions
    that the user input is passed to. This checks for the 
    appropriate responses with the minimal data required.
    """

    def setUp(self):
        """
        It is necessary to instantiate the data classes and extract the
        relevant dictionaries.
        This testing suite requires two socket connections.
        """
        self.test_data_true = dictionary_class_helper_true()
        self.test_data_false = dictionary_class_helper_false()
        self.sock_conn_valid = socketconnection.SocketConnection(self.test_data_true.car_id)
        self.sock_conn_invalid = socketconnection.SocketConnection(self.test_data_false.car_id)
        self.valid_dict = self.test_data_true.get_socket_dictionary()
        self.invalid_dict = self.test_data_false.get_socket_dictionary()
        print("Test suite: {}".format(type(self).__name__))

    def test_valid_cred(self):
        """
        Test valid credential response.
        """
        returned_dict = self.sock_conn_valid.validate_text_credentials(
            self.valid_dict["username"], 
            self.valid_dict["password"]
            )
        # self.assertEqual(self.valid_dict["username"], returned_dict["username"])
        self.assertEqual(returned_dict, False)
    def test_invalid_cred(self):
        """
        Test invalid credential response.
        """
        returned_dict = self.sock_conn_valid.validate_text_credentials(
            self.invalid_dict["username"], 
            self.invalid_dict["password"]
            )
        self.assertEqual(returned_dict, False)
    
    def test_valid_token(self):
        """
        Test valid token response.
        """
        returned_dict = self.sock_conn_valid.validate_face_credentials(
            self.valid_dict["usertoken"] 
            )
        # self.assertEqual(returned_dict["username"], self.valid_dict["username"])
        self.assertEqual(returned_dict, False)
    def test_invalid_token(self):
        """
        Test invalid token response.
        """
        returned_dict = self.sock_conn_valid.validate_face_credentials(
            self.invalid_dict["usertoken"] 
            )
        self.assertEqual(returned_dict, False)

    def test_invalid_car_cred(self):
        """
        Test invalid car but valid credentials.
        """
        returned_dict = self.sock_conn_invalid.validate_text_credentials(
            self.valid_dict["username"], 
            self.valid_dict["password"]
            )
        self.assertEqual(returned_dict, False)

    def test_invalid_car_token(self):
        """
        Test invalid car but valid token.
        """
        returned_dict = self.sock_conn_invalid.validate_face_credentials(
            self.valid_dict["usertoken"] 
            )
        self.assertEqual(returned_dict, False)

    # Helper information for setting values based on keys:
        # "action": self.action,
        # "car_id": self.car_id,
        # "username": self.username,
        # "password": self.password,
        # "usertoken": self.usertoken,
        # "info_date_time": self.info_date_time,
        # "current_location": self.current_location


class TestInvalidAction(unittest.TestCase):
    """
    This class tests edge cases resulting in an invalid action
    Basically send a random integer as the action that is not one of the
    accepted actions.
    """

    def setUp(self):
        """
        It is necessary to instantiate the data classes and extract the
        relevant dictionaries.
        """
        self.test_data_true = dictionary_class_helper_true()
        self.test_data_false = dictionary_class_helper_false()
        self.sock_conn_valid = socketconnection.SocketConnection(self.test_data_true.car_id)
        self.valid_dict = self.test_data_true.get_socket_dictionary()
        print("Test suite: {}".format(type(self).__name__))

    def test_invalid_action(self):
        """
        Vary loops through this to vary the extensiveness of the test.
        """
        action = random.randint(-10000,10000)
        if action < 1 or action > 4:
            test_dict = self.valid_dict
            test_dict["action"] = action
            returned_dict = self.sock_conn_valid.validation_returner(test_dict)
            self.assertEqual(returned_dict, False)


def dictionary_class_helper_true() -> agentdata.DictionaryConstructor:
    """
    This helper functions return dictionary class objects for testing purposes
    populated by correct values.
    To build tests that look at each element of the object,
    set the value directly, changing the object by one keyvalue at time via class level
    function calls.

    .. note:: This function returns an instantiation of a custom class - you must call the dictionary
        return function before passing to any socket calls.
    """
    # Set Data to be converted.
    date_to_use = datetime.datetime.now().isoformat()
    car_name = "car123"
    test_data = agentdata.DictionaryConstructor(car_name, date_to_use)
    action = 1
    username = "uname"
    password = "pword"
    usertoken = "5c0be87ed7434d69005f8bbd84cad8ae6abfd49121b4aaeeb4c1f4a2e2987711"
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
    """
    This helper functions return dictionary class objects for testing purposes
    populated by incorrect values.
    The only elements that does not change from a valid dictionary is the action.
    To build tests that look at each element of the object,
    set the value directly, changing the object by one keyvalue at time via class level
    function calls.

    .. note:: This function returns an instantiation of a custom class - you must call the dictionary
        return function before passing to any socket calls.
    """
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

if __name__ == "__main__":
    unittest.main()
"""
This module contains the classes that are used to
communicate with the master pi.

Instantiating the class has accepts one paramter - the :attr:`car_id`. 
The socket connection then sends a JSON object to the server.
This object is defined at both ends, and is based on a dictionary that contains
the :attr:`car_id` and the current time, as well as either of the username 
and password (text validation) or the user_token (face validation), or any
further attributes deemed relevant by the called function. See the individual
function for further details..
"""

# The two entry points for validation accept either the token from the face recognition file
# or the username and password (or equivalent) and then return the username or
# token respectively. The token is returned so that it can be used for future encoding
# of the pickle face recognition encoding file.

# The other entry point accepts nothing, and simply informs the master
# pi that the vehicle has been returned.

import socket
import ssl
import json
import time
from agentdata import DictionaryConstructor as DictionaryConstructor
from agentdata import DictionaryDateUpdater as DictionaryDateUpdater
import datetime
import utilities
# To consolidate logs into one location.
import logging
log = logging.getLogger(__name__)


class SocketConnection:
    """
    This class is instantiated with just the :attr:`car_id` and then the appropriate method
    must be called to achieve the desired result, passing in the appropriate
    objects. A dictionary is then constructed and returned using the :mod:`agentdata`
    module and then this is passed to the socket which returns a dictionary
    for the called method to act on.
    """

    def __init__(self, car_id: str):
        self.car_id = car_id

        # self.IP_ADDRESS = "127.0.0.1"
        # self.M_PI_PORT = 33333
        self.IP_ADDRESS = "220.240.169.117"
        self.M_PI_PORT = 33333        
        self.ADDRESS = (self.IP_ADDRESS, self.M_PI_PORT)

    def validate_text_credentials(self, username: str, password: str):
        """
        This function will send the username, password, car_id and date to
        the server for validation.
        """
        # Construct the dictionary using the DictionaryConstructor
        # object and methods, updating the relevant parameters.
        socket_dictionary_creator = DictionaryConstructor(
            self.car_id,
            datetime.datetime.now().isoformat()
            )
        socket_dictionary_creator.set_action(1)
        socket_dictionary_creator.set_username(username)
        socket_dictionary_creator.set_password(password)
        
        # Retrieve the dictionary.
        socket_dictionary = socket_dictionary_creator.get_socket_dictionary()
        log.info("Socket dictionary compiled: {}".format(socket_dictionary))

        # Return the response from the validation_returner.
        return self.validation_returner(socket_dictionary)

    def validate_face_credentials(self, user_token: str):
        """
        Validate the face recognition.
        """

        # Construct the dictionary
        log.info("Validating {}".format(user_token))
        socket_dictionary_creator = DictionaryConstructor(
            self.car_id, 
            datetime.datetime.now().isoformat()
            )
        socket_dictionary_creator.set_action(2)
        socket_dictionary_creator.set_usertoken(user_token)

        # Retrieve the dictionary and pass it to the socket sender
        socket_dict_tosend = socket_dictionary_creator.get_socket_dictionary()

        # Return the dictionary.
        return self.validation_returner(socket_dict_tosend)

    def validate_engineer(self, engineer_bluetooth: list):
        """
        Validate an engineer's bluetooth credentials.
        This constitutes Action 5 for communicaiton purposes.
        """

        # Construct the dictionary with the appropriate action (5)
        # and the set of bluetooth addresses.
        log.info("Validating engineer: {}".format(engineer_bluetooth))
        socket_dictionary_creator = DictionaryConstructor(
            self.car_id,
            datetime.datetime.now().isoformat()
        )
        socket_dictionary_creator.set_action(5)
        socket_dictionary_creator.set_engineer_bluetooth(engineer_bluetooth)

        # Retrieve the dictionary and pass it to the socket.
        socket_dict_tosend = socket_dictionary_creator.get_socket_dictionary()
        # Return the dictionary returned by the MP.
        return self.validation_returner(socket_dict_tosend)

    def validation_returner(self, dict_to_validate: dict):
        """
        Accepts a constructed dictionary from the two validation functions,
        sends it to the establish_connection for validation, and returns
        based on the response.
        """

        # Send dictionary to master pi, accepting the return
        socket_return = self.establish_connection(dict_to_validate)

        # Process the dictionary and return based on the outcome.
        #log.info("Socket returned action: {}".format(socket_return["action"]))
        if socket_return is None:
            # No response.
            return None

        log.info("Socket returned action: {}".format(socket_return["action"]))
        if socket_return["action"] == 4 or socket_return["action"] == 6:
            # Vehicle returned successfully, otherwise will
            # return false as there will be no username either.
            return True
        
        if socket_return["username"] is None:
            # Invalid Credentials
            return False
        # All good - return the dictionary.
        return socket_return

    def terminate_booking(self):
        """
        Updating the Master Pi when the booking has been concluded.
        This constitutes Action 4 for communication purposes.
        """

        # Create a dictionary object.
        socket_dictionary_creator = DictionaryConstructor(
            self.car_id, 
            datetime.datetime.now().isoformat()
            )
            # Update with the details for the end of a booking
        socket_dictionary_creator.set_action(4)
        clearutil = utilities.HelperUtilities()
        location = clearutil.get_location()
        socket_dictionary_creator.set_current_location(location)
        #log.info(socket_dictionary)

        # Create a socket object and return the returned dictionary.
        socket_dict_tosend = socket_dictionary_creator.get_socket_dictionary()
        log.info(socket_dict_tosend)
        return self.validation_returner(socket_dict_tosend)

    def terminate_engineer(self, engineer_code: str):
        """
        Updates the master pi when an engineer concludes their
        work. 
        This constitutes Action 6 for communication purposes.
        """

        # Create a dictionary to send
        socket_dictionary_creator = DictionaryConstructor(
            self.car_id,
            datetime.datetime.now().isoformat()
        )
        # Update dictionary with appropriate information.
        socket_dictionary_creator.set_action(6)
        socket_dictionary_creator.set_engineer_code(engineer_code)
        clearutil = utilities.HelperUtilities()
        location = clearutil.get_location()
        socket_dictionary_creator.set_current_location(location)

        # Retrieve the dictionary and send it to the mp.
        socket_dict_tosend = socket_dictionary_creator.get_socket_dictionary()
        log.info("Engineer Code Socket Dict: {}".format(socket_dict_tosend))
        return self.validation_returner(socket_dict_tosend)

    def establish_connection(self, dict_to_send: dict) -> dict:
        """
        This method is called by methods in this class for performing
        an action with the master pi. It accepts a dictionary (from :mod:`agentdata`)
        and returns a dictionary of the same type to be acted on.
        """

        # Convert the dictionary to a string json string object in utf-8.
        # This ensure that almost all special characters are preserved.
        encoded_dictionary = json.dumps(dict_to_send).encode("utf-8")

        # Open a socket and send the dictionary, then await a reply.
        returned_bytes = b""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as (socket_connection):
                socket_connection.connect(self.ADDRESS)
                print("Connected to Server.")
                socket_connection.sendall(encoded_dictionary)
                
                # Receive the data
                # TODO How do we exit this in a timely manner?
                print("Awaiting Response.")

                temporary_bytes = socket_connection.recv(1024)
                returned_bytes += temporary_bytes
                log.info("Socket connection response: {}".format(temporary_bytes))

                # while True:
                #     temporary_bytes = s.recv(1024)
                #     returned_bytes += temporary_bytes
                #     print("got something: {}".format(temporary_bytes))

                    # if not temporary_bytes:
                    #     print("Breaking")
                    #     break
                    # count = 0
                    # if not temporary_bytes:
                    #     sleep(1)
                    #     count += 1 
                    #     if count > 4:
                    #         print("Failed to contact server - try again later.")
                    #         break
        except ConnectionRefusedError as err:
            print("Unable to connect to server")
            log.exception("Server connection refused: {}".format(err))
            return None
        except Exception as e:
            log.exception(e)
            return None
                
        # Exit the context manager, closing the connection and convert
        # the bytes back to a dictionary.
        try: 
            returned_dictionary = json.loads(returned_bytes.decode("utf-8"))
            
            log.info("Dictionary returned from server: {}".format(returned_dictionary))

            # Update the returned dictionary to conform with the communication
            # standard, in case a date has been communicated in an ISO
            # format, and return to the calling function.
            if returned_dictionary["info_date_time"] is not None:
                log.info("Updating Socket Dictionary")
                try: 
                    update_dictionary = DictionaryDateUpdater(returned_dictionary["info_date_time"])
                    returned_dictionary["info_date_time"] = update_dictionary.get_python_date()
                except e:
                    print("Error converting dictionary!")
                    log.exception("Error converting dictionary: ".format(e))
            return returned_dictionary
        except TypeError as e:
            log.exception("Error reading dictionary: {}".format(e))
            return None
        except Exception as e:
            log.exception("Extreme error: {}".format(e))
            return None

if __name__ == "__main__":
    pass


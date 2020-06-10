# Module containing the server aspect of the socket connection.

import socket
import select
import json
from agentdata import DictionaryDateUpdater as DictionaryDateUpdater
from agentdata import DictionaryConstructor as DictionaryConstructor
from masterpiresponder import MasterResponder as MasterResponder


class SocketResponder():
    """
    The primary class in this module (though the not main method), this 
    class is responsible for listening and accepting dictionaries, then
    passing them on to the :class:`DictionaryInterpreter` class and call the 
    internal function for the appropriate action to be undertaken.

    .. note:: It is important to set the correct public facing IP address and port,
        as it is not always possible for the function to determine this automatically.
        
    .. warning:: Certain technologies have been found to impede a consistent connection.
        These include Proxies, Firewalls, and CGNAT implemented by certain retail internet
        service providers.
    """

    def __init__(self):
        self.IP_ADDRESS = "192.168.1.109"
        self.M_PI_PORT = 33333
        self.ADDRESS = (self.IP_ADDRESS, self.M_PI_PORT)
        self.socket_queue = 15


    def accept_connections(self):
        """
        Creates a socket that listens on a defined port at the defined IP for 
        connection from an Agent.
        """
        # Create an instance of socket with the predefined IP.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            #server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Set the socket to reuse the same local port in case the application
            # needs to be restarted. See: https://docs.python.org/3.3/library/socket.html
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Bind the socket to the designated IP and Port 
            # socket.gethostname() is problematic, so manually setting is advised. 
            server_socket.bind(self.ADDRESS)
            # Set the socket to listen mode with the designated queue
            server_socket.listen(self.socket_queue)

            # Then loop indefinitely accepting and acting on connections.
            while True:
                # Accept a connection.
                client_conn, client_addr = server_socket.accept()
                # TODO IF we are validating connections, it is necessary 
                # here to validate that the client_addr is expected. This
                # could be done by storing a list of the known IPs and 
                # closing the connection if it isn't valid
                # if client_addr is not in list: client_conn.close()
                
                # Create a binary file for accepting the socket data, and 
                # attempt to receive the data.
                received_bytes = b""
                with client_conn:
                    print("Master receiving data....")
                    temporary_bytes = client_conn.recv(1024)
                    received_bytes += temporary_bytes

                    transmitted_dictionary = json.loads(received_bytes.decode("utf-8"))
                    print("Received dictionary: {}".format(transmitted_dictionary))
                    # TODO When receiving the dictionary, we have to convert the 
                    # date value back to datetime as it is in iso format for sending.
                    if transmitted_dictionary["info_date_time"] is not None:
                        date_updater = DictionaryDateUpdater(transmitted_dictionary["info_date_time"])
                        transmitted_dictionary["info_date_time"] = date_updater.get_python_date()
                        print("Dictionary updated: {}".format(transmitted_dictionary))
                    
                    # Create a dictionary interpreter and from this create a 
                    # dictionary to return to the Agent Pi.
                    dictionary_actor = DictionaryInterpreter(transmitted_dictionary)
                    dictionary_to_return = dictionary_actor.interpret_dictionary()

                    # Convert the dictionary to JSON
                    # TODO This could probably be moved to a module so both ends can 
                    # perform the same function...?
                    encoded_dictionary = json.dumps(dictionary_to_return).encode("utf-8")
                    print("Dictionary to return: {}".format(encoded_dictionary))
                    client_conn.sendall(encoded_dictionary)
                    print("Response complete! \n")


# Instantiated with a dictionary, this class acts based on the contents of a
# dictionary and its sole function returns a modified dictionary to the socket.
class DictionaryInterpreter():
    """
    This class is instantiated with a diciontionary from an Agent.
    The sole function interprets this dictionary and passes it to the
    appropriate class/function to be acted on, or acts on an invalid action.
    """
    def __init__(self, received_dict: dict):
        self.received_dict = received_dict

    def interpret_dictionary(self):
        """        
        This is the entry point for this class - it returns a the result from calling
        a method in the :class:`MasterResponder`, that acts on the dictionary and returns it.
        This is a modified version of the dictioonary that was passed into the
        instantiation of the owning class. It determines what
        function to call based on the contents of the transmitted dictionary.
        """
        responder = MasterResponder(self.received_dict)
        if self.received_dict["action"] == 1:
            # Validate a text credential and return dictionary
            print("returning....")
            return responder.validate_credentials()
        elif self.received_dict["action"] == 2:
            # Validate a face recognition token and return dictionary
            print("Validating face and returning....")
            return responder.validate_face()
        elif self.received_dict["action"] == 3:
            # Update a face recognition token and return dictionary
            pass
        elif self.received_dict["action"] == 4:
            # Return the vehicle and return dictionary
            print("Returning a vehicle....")
            return responder.return_vehicle()
        elif self.received_dict["action"] == 5:
            # Validate an engineer and return dictionary.
            print("Validating engineer bluetooth credentials and returning....")
            return responder.validate_engineer()
        elif self.received_dict["action"] == 6:
            # Return the vehicle from an engineer.
            print("Engineer attempting to return vehicle")
            return responder.engineer_return()
        else: 
            # Do nothing and return an empty dicitonary.
            print("Invalid option!")
            return responder.invalid_action()



class Main():
    def start(self):
        master_responder = SocketResponder()
        master_responder.accept_connections()

if __name__ == "__main__":
    socket_responder = Main()
    socket_responder.start()
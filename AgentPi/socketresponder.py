# Module containing the server aspect of the socket connection.

import socket
import select
import pickle


class SocketResponder():
    def __init__(self):
        self.IP_ADDRESS = "127.0.0.1"
        self.M_PI_PORT = 33333

    def accept_connections()
    while True:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((socket.gethostname(), 33333)
        server_socket.listen(5)



        # TODO When recieving the dictionary, we have to convert the 
        # date value back to datetime as it is in iso format for sending.
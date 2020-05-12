# Module containing the server aspect of the socket connection.

import socket
import select
import pickle


class SocketResponder():

    while True:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((socket.gethostname(), 33333)
        server_socket.listen(5)
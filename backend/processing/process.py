import socket
import os

address = '0.0.0.0' 
port = 32017

sock = socket.socket()

sock.bind((address, port))
sock.listen()

while (True):
    (connection, client_address) = sock.accept()
    print("Opened a connection with {}".format(client_address))

    data_from_client = connection.recv(4096)
    print("Got data from the client:")
    print(data_from_client)

    connection.send("Got your message".encode())

    connection.close()
    print("Closed the connection with {}".format(client_address))

import socket
import os

#
# This file is provided as a minimial example for how the backend must
# interact with the rest of Watercolor.
# It implements the simplest possible backend - it accepts a string, prints
# it to stdout, then echoes back a hardcoded string.
# You can probably modify this to create the actual backend.
#
# This does not depend on any external libraries. 
# If you need the backend to depend on anything, you must add it to the
# environment.yml and then add an import statement here.
#

# The listening address MUST be 0.0.0.0.
address = '0.0.0.0' 

# The port is arbitrary, but if it is ever changes it MUST also be updated
# in each of the deployment/service specs. So I'd just leave it.
port = 32017

sock = socket.socket()

# The server is listening at 32017 and will accept queries from any IP
# (security hole?)
sock.bind((address, port))
sock.listen()

while (True):
    # This starts the connection.
    # The program will wait at the .accept call until it recieves a message.
    # The "connection" variable is a NEW socket between this server and the
    # connected client. Use it to send data back and forth, NOT "sock".
    (connection, client_address) = sock.accept()
    print("Opened a connection with {}".format(client_address))

    # This is how to recieve data.
    # The 4096 is just the internal buffer size and is NOT the amount of 
    # data recieved.
    data_from_client = connection.recv(4096)

    # Since the sockets connect with raw bytes over TCP, we cannot directly
    # send/recieve strings. We need to encode/decode them into/from their raw
    # byte representation, which is what actually gets sent over the wire.
    # Here, we print "data_from_client" without decoding it. But if we wanted
    # the string itself, we'd need to do:
    # data_from_client.decode()
    print("Got data from the client:")
    print(data_from_client)

    # To send a string, we must encode it. See the above comment.
    connection.send("Got your message".encode())

    # ALWAYS CLOSE THE CONNECTION WHEN YOU'RE DONE SENDING DATA.
    # Networking 101, friends (?)
    connection.close()

    print("Closed the connection with {}".format(client_address))


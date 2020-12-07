import socket
import os

#import cv2
#from cv2 import dnn_superres
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

# found on stackoverflow: https://stackoverflow.com/questions/27428936/python-size-of-message-to-send-via-socket
def get_msg_size(conn):
    buf = b''
    while True:
        c = conn.recv(1)
        if c == b'|':
            return int(buf.decode())
        buf += c
def upscale(b64str):
    sr = dnn_superres.DnnSuperResImpl_create()

    image = cv2.imread('./examples/input.jpg')

    model_path = "./models/EDSR_x3.pb"
    sr.readModel(model_path)

    #"edsr" or "fsrcnn"
    sr.setModel("edsr", 3)

    result = sr.upsample(image)

    cv2.imwrite("./examples/output/input_scaled.jpg", result)
while (True):
    try:
        # This starts the connection.
        # The program will wait at the .accept call until it recieves a message.
        # The "connection" variable is a NEW socket between this server and the
        # connected client. Use it to send data back and forth, NOT "sock".
        (connection, client_address) = sock.accept()
        print("Opened a connection with {}".format(client_address), flush=True)
        
        m_size = get_msg_size(connection)
        print("Size of message: ", m_size, flush=True)
        connection.send("Recieved size.".encode())

        # This is how to recieve data.
        # The 4096 is just the internal buffer size and is NOT the amount of 
        # data recieved.
        tot_data = b''
        #continue to recieve data we have recieved the whole message
        while(len(tot_data) < m_size):
            data = connection.recv(4096)
            #print("data chunk size: ", type(data), len(data), flush=True)
            tot_data += data
            #print("tot_data size: ", type(tot_data), len(tot_data), flush=True)
        print(f"finished recieving data\ntot_data size: {len(tot_data)}", flush=True)
       
        reply_size = str(len(tot_data)) + '|'
        connection.send(reply_size.encode())
        s_reply = connection.recv(128)
        print(f"Sent size of reply_data to API and recieve reply: {s_reply.decode()}", flush=True)

        connection.sendall(tot_data)
        reply = connection.recv(128)
        print(f"Sent Data to API and recieved reply: {reply.decode()}", flush=True)
    except Exception as e:
        print(f"Caught an Exception: {e}", flush=True)
    # ALWAYS CLOSE THE CONNECTION WHEN YOU'RE DONE SENDING DATA.
    # Networking 101, friends (?)
    finally:
        connection.close()
        print("Closed the connection with {}".format(client_address), flush=True)


import socket
import os
import traceback

import cv2
from cv2 import dnn_superres
import base64
import numpy as np
from pathlib import Path
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

#sends reply size and data
def send_reply(data):
    reply_size = str(len(data)) + '|'
    connection.send(reply_size.encode())
    s_reply = connection.recv(128)
    print(f"Sent size of reply_data to API and recieve reply: {s_reply.decode()}", flush=True)

    connection.sendall(data)
    reply = connection.recv(128)
    print(f"Sent Data to API and recieved reply: {reply.decode()}", flush=True)

#converts base64 string to img
#found on stack overflow: https://stackoverflow.com/questions/17170752/python-opencv-load-image-from-byte-string
def str_to_img(img_bytes):
    img_original = base64.b64decode(img_bytes)
    print(f"decoded {img_original[0:10]}")
    img_as_np = np.frombuffer(img_original, dtype=np.uint8)
    #img_as_np = np.fromstring(string, np.uint8)
    print(f"decoded np: {img_as_np}")
    img = cv2.imdecode(img_as_np, cv2.IMREAD_UNCHANGED)
    print(f"decoded img len: {len(img)}")
    return img


#converts img to base64 string to send back
def img_to_str(img, img_type):
    print(f"converting image with shape, {img.shape}, to string")
    _, img_encoded = cv2.imencode(img_type, img)
    str_enc = base64.b64encode(img_encoded).decode()
    print(f"finished converting image to string:  {len(str_enc)}")
    return str_enc

#upscales the input image which is a cv2 images
def upscale(image):
    sr = dnn_superres.DnnSuperResImpl_create()

    edsr_model_path = Path("/watercolor-processing/models/EDSR_x3.pb")
    fsr_model_path = Path("/watercolor-processing/models/FSRCNN_x3.pb")

    #print("model path: ", model_path, flush=True)
    sr.readModel(str(fsr_model_path))

    #"edsr" or "fsrcnn"
    sr.setModel("fsrcnn", 3)
    print(f"started upscaling image with shape: {image.shape}")
    result = sr.upsample(image)
    print(f"finished upscaling image: {result.shape}")
    return result
while (True):
    try:
        print("-"*25 + "\n\n")
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
        
        #add the equal signs to  fix padding issue i.e. b'==='
        img = str_to_img(tot_data + b'===')
        print(f"img dim: {img.shape}")
        #image is png so trim alpha channel for now
        alpha_channel = None
        is_png = False
        if(img.shape[2] == 4):
            is_png = True
            alpha_channel = img[:,:,3]
            #trim alpha channel
            img = img[:,:,0:3]
            print(f"PNG-->new_shape : {img.shape}")

        res_img = upscale(img) 
        
        if(is_png):
            #add back the alpha channel
            res_img = cv2.cvtColor(res_img, cv2.COLOR_BGR2BGRA)
            #res_img[:,:,3] = alpha_channel
            print(f"Result PNG-->new_shape: {res_img.shape}")
        img_suffix = '.png' if is_png else '.jpg'
        print(f"suffix: {img_suffix}") 
        res_str = img_to_str(res_img, img_suffix)

        send_reply(res_str.encode())   
    except:
        traceback.print_exc()
        #print(f"Caught an Exception: {e}\ntype: {type(e)}", flush=True)
    # ALWAYS CLOSE THE CONNECTION WHEN YOU'RE DONE SENDING DATA.
    # Networking 101, friends (?)
    finally:
        connection.close()
        print("Closed the connection with {}".format(client_address), flush=True)


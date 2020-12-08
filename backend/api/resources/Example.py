from flask_restful import Resource
from flask import request

import socket
import os

backend_address = "127.0.0.1"
backend_port = 32017
try:
    backend_address = os.environ['WTC_PROCESS_SERVICE_HOST']
    backend_port = int(os.environ['WTC_PROCESS_SERVICE_PORT'])
except KeyError:
    pass

def get_msg_size(conn):
    buf = b''
    while True:
        c = conn.recv(1)
        #print(c, flush=True)
        if c == b'|':
            #print("finished recieving size", flush=True)
            return int(buf.decode())
        buf += c
class Example(Resource):
    def get(self):
        print("Received GET request: ", request.json,flush=True)
        return {
            'data': 'you ran a GET request',
            'args': request.json
        }

    def post(self):
        print("Received POST request: ", flush=True)
        try:
            # this is where we'll mess with the images
            # ----
            sock = socket.socket() # socket socket? socket.

            print("connecting to {}:{}".format(backend_address, backend_port), flush=True)
            sock.connect((backend_address, backend_port))
            
            images = []
            # Process the images by sending them to the processing backend.
            for image_uri in request.json['images']:
                #image_uri has a header and data seperated by a ','
                header, data = image_uri.split(",", 1)
                print("header: ", header)
                print("data[0:100]: ", data[0:100])
                #encoded is a utf-8 encoded version of the base64 string representing the image
                encoded = data.encode()
                enc_size = len(encoded)
                #send size of message first --  send "size|"
                s_enc_size = str(enc_size) + '|'
                sock.sendall(s_enc_size.encode())
                reply = sock.recv(128)
                print(f"sent size and recieved reply: {reply.decode()}", flush=True)

                print("image length: ", enc_size, flush=True)
                # assumes that "image" is a string, hopefully of the base64 variety!
                # this will cause a TypeError if "image" is not a bytes-like object.
                sock.sendall(encoded)
                print("Sent one image to backend", flush=True)
                
                ''' recieve reply data from backend '''
                reply_size = get_msg_size(sock) 
                sock.send("Recieved reply_size".encode()) 
                print(f"Recieved reply_size: {reply_size}", flush=True)

                ''' add back uri header '''
                reply_data = header + ','
                reply_data = reply_data.encode()
                while len(reply_data) < reply_size:
                    reply_data += sock.recv(4096)
                print("reply_data size: ", len(reply_data), flush=True)
                sock.send("recieved data from backend".encode())
                
                print(f"beginning of reply_data: {reply_data[0:100]}")
                images.append(reply_data.decode())
            print("Finished sending data to backend.", flush=True)
            #print("Recieved response from backend: {}".format(reply_data.decode()), flush=True)
            #reply = sock.recv(4096)
            #print("Recieved response  from backend: {}".format(reply.decode()), flush=True)
        except Exception as e:
            print(f"Caught an Exception:{e}", flush=True)
        finally:
            sock.close()
            print("closing socket", flush=True)
        # ----
        print("Sending response to client.")
        return {
            'id': request.json['id'], # echo back the id
            'images': images, # for now, echo back the images
            'backend-response': reply.decode()
        }

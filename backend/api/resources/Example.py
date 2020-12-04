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

class Example(Resource):
    def get(self):
        print("Received GET request: " + str(request.json), flush=True)
        return {
            'data': 'you ran a GET request',
            'args': request.json
        }
    def post(self):
        print("Received POST request: " + str(request.json), flush=True)

        # this is where we'll mess with the images
        # ----
        sock = socket.socket() # socket socket? socket.

        print("connecting to {}:{}".format(backend_address, backend_port))
        sock.connect((backend_address, backend_port))
        
        # Process the images by sending them to the processing backend.
        for image in request.json['images']:
            # assumes that "image" is a string, hopefully of the base64 variety!
            # this will cause a TypeError if "image" is not a bytes-like object.
            sock.send(image.encode()) 

        reply = sock.recv(4096)
        print("Recieved response from backend: {}", reply.decode())
        sock.close()
        # ----
        return {
            'id': request.json['id'], # echo back the id
            'images': request.json['images'], # for now, echo back the images
            'backend-response': reply.decode()
        }

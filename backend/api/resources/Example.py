from flask_restful import Resource
from flask import request

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
        return {
            'id': request.json['id'], # echo back the id
            'images': request.json['images'] # for now, echo back the images
        }

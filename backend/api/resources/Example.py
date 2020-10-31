from flask_restful import Resource

class Example(Resource):
    def get(self):
        return {
            'data': 'hello from resource'
        }
    def post(self):
        pass

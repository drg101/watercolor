from flask import Flask
from flask_restful import Api
#import resources here
from api.resources.example import Example

#setting up app
app = Flask(__name__)
api = Api(app)

#add resources to api here
api.add_resource(Example, '/Example')
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
#import resources here
from resources.Example import Example

#setting up app
app = Flask(__name__)
CORS(app)
api = Api(app)

#add resources to api here
api.add_resource(Example,'/', '/Example')
if __name__ == '__main__':
    #running app externally
    app.run(host='0.0.0.0')
    #running app for localhost
    #app.run(debug=True)

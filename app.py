from flask import Flask
from flask_restful import Api
from SpartaHack_API_2019 import config # pylint: disable=invalid-syntax
load_env_variables()


app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)#loading config data into flask app from config.py

api = Api(app)

if __name__ == '__main__': #running on local server. This needs to change for prod
    app.run(debug=True)
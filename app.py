from flask import Flask
from flask_restful import Api
from SpartaHack_API_2019.config import load_env_variables, DevelopmentConfig, ProdConfig
load_env_variables() #loading enviornment variables


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)#loading config data into flask app from config.py

api = Api(app)

if __name__ == '__main__': #running on local server. This needs to change for prod
    app.run(debug=True)
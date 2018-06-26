from flask import Flask
from flask_restful import Api
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from SpartaHack_API_2019.config import load_env_variables, DevelopmentConfig, ProdConfig
load_env_variables() #loading enviornment variables


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)#loading config data into flask app from config.py

api = Api(app)
db = SQLAlchemy(app)
task_queue=Celery("SpartaHack_API_2019",broker=app.config["CELERY_BROKER_URL"])

if __name__ == '__main__': #running on local server. This needs to change for prod
    app.run(debug=True)
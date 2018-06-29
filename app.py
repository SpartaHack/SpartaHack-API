from flask import Flask
from flask_restful import Api
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from config import load_env_variables, DevelopmentConfig, ProdConfig
load_env_variables() #loading enviornment variables

from SpartaHack_API_2019.resources.faqs import Faqs_RUD
from SpartaHack_API_2019.resources.faqs import Faqs_CR

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)#loading config data into flask app from config.py

api = Api(app)

db = SQLAlchemy(app)
#db.reflect(app=app)#to reflect on the already defined database

task_queue=Celery("SpartaHack_API_2019",broker=app.config["CELERY_BROKER_URL"])

api.add_resource(Faqs_RUD,"/faqs/<int:faq_id>")
api.add_resource(Faqs_CR,"/faqs/")

if __name__ == '__main__': #running on local server. This needs to change for prod
    app.run(debug=True)
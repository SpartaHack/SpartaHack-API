from flask import Flask, jsonify, make_response,request, g
from flask_restful import Api
from celery import Celery
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from common.utils import unauthorised,headers,not_found

from config import load_env_variables, DevelopmentConfig, ProdConfig

#loading enviornment variables
load_env_variables()

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)#loading config data into flask app from config object.
api = Api(app)

#reflecting classes
print("Reflecting classes...")
Base = automap_base()
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"],pool_size=20,max_overflow=20,pool_pre_ping=True)
Base.prepare(engine, reflect=True)
print("Classes reflected...")

@app.errorhandler(404)
def not_found(error):
    """
    Custom response object for endpoints that have not been defined yet.
    """
    resp = make_response(jsonify(not_found), 404)
    resp.headers.extend(headers)
    return resp

@app.before_request
def create_session():
    """
    Before processing any request. Create a session by checking out a connection from the connection pool.
    Also set request global variables to be accessed for the life time of the request

    """
    g.session = Session(engine)
    g.Base = Base

@app.after_request
def commit_and_close_session(resp):
    """
    After all the processing is done. Commit the changes and close the session to return the connection object back to the connection pool.
    """
    g.session.commit()
    g.session.close()
    return resp

#loading resources
from resources.faqs import Faqs_RUD
from resources.faqs import Faqs_CR
from resources.announcements import Announcements_RUD
from resources.announcements import Announcements_CR
from resources.hardware import Hardware_RUD
from resources.hardware import Hardware_CR

@api.representation('application/json')
def ret_json(data, code, headers=None):
    """
    Create proper request object based on the return dictionary.
    """
    if code == 204:
        resp = make_response('', code)
    else:
        resp = make_response(jsonify(data), code)
    resp.headers.extend(headers)
    return resp

#might only need this for email sending so that email sending does not clog up the resources
task_queue=Celery("SpartaHack_API_2019",broker=app.config["CELERY_BROKER_URL"])

#adding resources. Just flask thingss :)
api.add_resource(Faqs_RUD,"/faqs/<int:faq_id>")
api.add_resource(Faqs_CR,"/faqs")
api.add_resource(Announcements_RUD,"/announcements/<int:announcement_id>")
api.add_resource(Announcements_CR,"/announcements")
api.add_resource(Hardware_RUD,"/hardware/<int:hardware_id>")
api.add_resource(Hardware_CR,"/hardware")

@app.route("/")
def helloworld():
    """
    For flask app test and general info about the API.
    Will also be used to check if the api is live or not on the slack hook
    """
    return jsonify({"Organisation":"SpartaHack",
                    "Backend Developers":"Yash, Jarek",
                    "Frontend Developers":"Harrison, Jessica, Jarek",
                    "Contact":"hello@spartahack.com",
                    "Version":"0.2.0"})

if __name__ == '__main__': #running on local server. This needs to change for prod
    app.run(debug=True)
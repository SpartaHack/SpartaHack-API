import flask_restful
from celery import Celery
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from flask import Flask, jsonify, make_response, request, g

import os

class Api(flask_restful.Api):
    def __init__(self, *args, **kwargs):
        super(Api, self).__init__(*args, **kwargs)
        self.representations = {
            # 'application/xml': ret_xml,
            # 'text/html': ret_html,
            # 'text/csv': ret_csv,
            'application/json': self.ret_json,
        }

    def ret_json(self, data, code, headers=None):
        """
        Create proper request object based on the return dictionary.
        """
        if code == 204:
            resp = make_response('', code)
        else:
            resp = make_response(jsonify(data), code)
        resp.headers.extend(headers)
        return resp

    # def ret_xml(self, data, code, headers=None):
    #     pass

    # def ret_html(self, data, code, headers=None):
    #     pass

    # def ret_csv(self, data, code, headers=None):
    #     pass

api = Api()

#initializing SQLAlchemy Base object
print("Reflecting classes...")
Base = automap_base()
engine = create_engine(os.environ['DEV_DATABASE_URL'],pool_size=20,max_overflow=20,pool_pre_ping=True)
Base.prepare(engine, reflect=True)
print("Classes reflected...")

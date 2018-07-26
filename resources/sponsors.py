from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from flask import request,jsonify,g
from datetime import datetime
from sqlalchemy import exists,and_
from sqlalchemy.orm.exc import NoResultFound
from common.json_schema import Sponsor_Schema
from common.utils import headers,is_logged_in,has_admin_privileges
from common.utils import bad_request,unauthorized,forbidden,not_found,internal_server_error,unprocessable_entity,conflict

class Sponsor_RUD(Resource):
    def get(sponsor_id):
        pass

    def put(sponsor_id):
        pass

    def delete(sponsor_id):
        pass

class Sponsor_CR(Resource):
    def post():
        pass

    def get():
        pass
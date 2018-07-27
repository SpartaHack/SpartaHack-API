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
        #using get instead of query and it is marginally faster than filter
        #check for multiple entries need to be done at POST and not during GET or PUT or DELETE
        try:
            sponsor = g.session.query(g.Base.classes.sponsors).get(sponsor_id)
        except Exception as err:
            print(type(err))
            print(err)
            return (internal_server_error,500,headers)

        if hardware_item:
            ret = Sponsor_Schema().dump(sponsor).data
            return (ret,200,headers)
        else:
            return (not_found,404,headers)

    def put(sponsor_id):
        pass

    def delete(sponsor_id):
        pass

class Sponsor_CR(Resource):
    def post():
        pass

    def get():
        pass
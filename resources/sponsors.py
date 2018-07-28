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
    """
    For GET UPDATE and DELETE for specific sponsor id
    """
    def get(self,sponsor_id):
        """
        GET the sponsor details based on specific sponsor_id
        """
        #using get instead of query and it is marginally faster than filter
        #check for multiple entries need to be done at POST and not during GET or PUT or DELETE
        try:
            sponsor = g.session.query(g.Base.classes.sponsors).get(sponsor_id)
        except Exception as err:
            print(type(err))
            print(err)
            return (internal_server_error,500,headers)

        if sponsor:
            ret = Sponsor_Schema().dump(sponsor).data
            return (ret,200,headers)
        else:
            return (not_found,404,headers)

    def put(self,sponsor_id):
        pass

    def delete(self,sponsor_id):
        pass

class Sponsor_CR(Resource):
    def post(self):
        pass

    def get(self):
        """
        GET all the announcements at a time.
        """
        try:
            all_sponsors = g.session.query(g.Base.classes.sponsors).all()
            ret = Sponsor_Schema(many = True).dump(all_sponsors).data
            return (ret,200,headers)
        except Exception as err:
            print(type(err))
            print(err)
            return (internal_server_error,500,headers)
from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from flask import request,jsonify,g
from datetime import datetime
from sqlalchemy import exists,and_
from sqlalchemy.orm.exc import NoResultFound
from common.json_schema import Application_Schema
from common.utils import headers,is_logged_in,has_admin_privileges
from common.utils import bad_request,unauthorized,forbidden,not_found,internal_server_error,unprocessable_entity,conflict

class Applications_RU(Resource):
    """
    For GET PUT for specific faq
    get http headers using request.headers.get("header_name")
    """
    def get(self,application_id):
        """
        GET the application details based on specific application_id
        """
        #using get instead of filter and it is marginally faster than filter
        #check for multiple entries need to be done at POST and not during GET or PUT or DELETE
        try:
            application = g.session.query(g.Base.classes.applications).get(application_id)
        except Exception as err:
            print(type(err))
            print(err)
            return (internal_server_error,500,headers)

        if application:
            ret = Application_Schema().dump(application).data
            return (ret,200,headers)
        else:
            return (not_found,404,headers)

    def put(self,application_id):
        """
        Update the application. Required data: TODO
        """
        pass

class Applications_CR(Resource):
    """
    To create new hardware using POST and read all hardware items
    """
    def post(self):
        """
        Create new application. Required data: TODO
        """
        pass

    def get(self):
        """
        GET all the applications at a time.
        """
        try:
            all_applications = g.session.query(g.Base.classes.applications).all()
            ret = Application_Schema(many = True).dump(all_applications).data
            return (ret,200,headers)
        except Exception as err:
            print(type(err))
            print(err)
            return (internal_server_error,500,headers)

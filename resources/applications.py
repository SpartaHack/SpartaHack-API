from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from flask import request,jsonify,g
from datetime import datetime
from sqlalchemy import exists,and_
from sqlalchemy.orm.exc import NoResultFound
from common.json_schema import Schedule_Schema
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
        pass

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
        pass

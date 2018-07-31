from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from flask import request,jsonify,g
from datetime import datetime
from sqlalchemy import exists,and_
from sqlalchemy.orm.exc import NoResultFound
from common.json_schema import Schedule_Schema
from common.utils import headers,is_logged_in,has_admin_privileges
from common.utils import bad_request,unauthorized,forbidden,not_found,internal_server_error,unprocessable_entity,conflict

class Schedule_RUD(Resource):
    """
    For GET UPDATE and DELETE for specific hardware id
    """
    def get(self,schedule_id):
        """
        GET the hardware details based on specific hardware_id
        """
        pass

    def put(self,schedule_id):
        """
        update the hardware. Required data: item, lender, quantity
        """
        pass

    def delete(self,schedule_id):
        """
        DELETE request to delete hardware based on specific hardware_id. This is new from the old api.
        """
        pass

class Schedule_CR(Resource):
    """
    To create new hardware using POST and read all hardware items
    """
    def post(self):
        """
        Create new hardware. Required data: item,lender, quantity
        """
        pass

    def get(self):
        """
        GET all the announcements at a time.
        """
        pass
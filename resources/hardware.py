from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from flask import request,jsonify,g
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from common.json_schema import Hardware_Schema
from common.utils import headers,is_logged_in,has_admin_privileges
from common.utils import bad_request,unauthorised,forbidden,not_found,internal_server_error,unprocessable_entity

class Hardware_RUD(Resource):
    """
    For GET UPDATE and DELETE for specific hardware id
    """
    def get(self,hardware_id):
        hardware_item = g.session.query(g.Base.classes.hardware).get(hardware_id)
        if hardware_item:
            ret = Hardware_Schema().dump(hardware_item).data
            return (ret,200,headers)
        else:
            return (not_found,404,headers)

    def put(self,hardware_id):
        pass

    def delete(self,hardware_id):
        pass

class Hardware_CR(Resource):
    """
    To create new hardware using POST and read all hardware items
    """
    def get(self):
        pass

    def post(self):
        pass
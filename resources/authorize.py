from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from flask import request,jsonify,g
from datetime import datetime
from sqlalchemy import exists,and_
from sqlalchemy.orm.exc import NoResultFound
from common.json_schema import Authorize_Schema, User_Schema
from common.utils import headers,is_logged_in,has_admin_privileges,waste_time,verify_pass
from common.utils import bad_request,unauthorized,forbidden,not_found,internal_server_error,unprocessable_entity,conflict
import random
import secrets
from authlib.jose import jwt

class Authorize_CD(Resource):
    """
    For POST for specific authorization request
    get http headers using request.headers.get("header_name")
    """

    def post(self):
        """
        for POST for authorize
        """
        try:
            data = request.get_json(force=True)
        except BadRequest:
            return (bad_request,400,headers)


         # *request data validation. Check for empty fields will be done by frontend
        validation = Authorize_Schema().validate(data)
        if validation:
            unprocessable_entity["error_list"]=validation
            return (unprocessable_entity,422,headers)

        jwt = data["id_token"]
        
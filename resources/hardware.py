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
        #check if data from request is serializable
        try:
            data = request.get_json(force=True)
        except BadRequest:
            return (bad_request,400,headers)

        #data validation
        if Hardware_Schema().validate(data):
            return (unprocessable_entity,422,headers)

        #check if user has admin privileges
        user_status,user = has_admin_privileges()
        if user_status == "no_auth_token":
            return (bad_request,400,headers)

        if user_status == "not_logged_in":
            return (unauthorised,401,headers)

        if user_status == True:
            hardware_item = g.session.query(g.Base.classes.hardware).get(hardware_id)
            if hardware_item:
                hardware_item.item = data["item"]
                hardware_item.lender = data["lender"]
                hardware_item.quantity = data["quantity"]
                hardware_item.updated_at = datetime.now()
                ret = Hardware_Schema().dump(hardware_item).data
                return (ret,200,headers)
            else:
                return (not_found,404,headers)

    def delete(self,hardware_id):
        user_status,user = has_admin_privileges()
        if user_status == "no_auth_token":
            return (bad_request,400,headers)

        if user_status == "not_logged_in":
            return (unauthorised,401,headers)

        if user_status == True:
            try:
                g.session.query(g.Base.classes.hardware).filter(g.Base.classes.hardware.id == hardware_id).one()
                g.session.query(g.Base.classes.hardware).filter(g.Base.classes.hardware.id == hardware_id).delete()
                return ("",204,headers)
            except NoResultFound:
                return (not_found,404,headers)
            except:
                return (internal_server_error,500,headers)
        else:
            return (forbidden,403,headers)

class Hardware_CR(Resource):
    """
    To create new hardware using POST and read all hardware items
    """
    def get(self):
        """
        GET all the annoucements at a time.
        """
        try:
            all_hardware = g.session.query(g.Base.classes.hardware).all()
            ret = Hardware_Schema(many = True).dump(all_hardware).data
            return (ret,200,headers)
        except:
            return (internal_server_error,500,headers)

    def post(self):

        pass
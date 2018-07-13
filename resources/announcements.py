from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from flask import request,jsonify,g
from sqlalchemy.orm.exc import NoResultFound
from common.json_schema import Announcement_Schema
from common.utils import headers,is_logged_in,has_admin_privileges
from common.utils import bad_request,unauthorised,forbidden,not_found,internal_server_error,unprocessable_entity

class Announcements_RUD(Resource):
    """
    For GET PUT and DELETE for specific announcement
    """
    def get(self,announcement_id):
        #get announcement by announcement id. Trying get() this time rather than filter to see which one runs better
        announcement = g.session.query(g.Base.classes.announcements).get(announcement_id)
        if announcement:
            ret = Announcement_Schema().dump(announcement).data
            return (ret,200,headers)
        else:
            return (not_found,404,headers)

    def put(self,announcement_id):
        pass

    def delete(self,announcement_id):
        pass

class Announcements_CR(Resource):
    """
    For GET PUT and DELETE for specific announcement
    """
    def get(self):
        try:
            all_announcements = g.session.query(g.Base.classes.announcements).all()
            ret = Announcement_Schema(many = True).dump(all_announcements).data
            return (ret,200,headers)
        except:
            return (internal_server_error,500,headers)

    def post(self):
        pass
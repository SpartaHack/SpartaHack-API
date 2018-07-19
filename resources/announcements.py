from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from flask import request,jsonify,g
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from common.json_schema import Announcement_Schema
from common.utils import headers,is_logged_in,has_admin_privileges
from common.utils import bad_request,unauthorized,forbidden,not_found,internal_server_error,unprocessable_entity

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
        """
        updating announcements. Required things - title, description, pinned
        """
        #check if data from request is serializable
        try:
            data = request.get_json(force=True)
        except BadRequest:
            return (bad_request,400,headers)

        #data validation
        if Announcement_Schema().validate(data):
            return (unprocessable_entity,422,headers)

        #check if user has admin privileges
        user_status,user = has_admin_privileges()
        if user_status == "no_auth_token":
            return (bad_request,400,headers)

        if user_status == "not_logged_in":
            return (unauthorized,401,headers)

        if user_status == True:
            announcement = g.session.query(g.Base.classes.announcements).get(announcement_id)
            if announcement:
                announcement.title = data["title"]
                announcement.description = data["description"]
                announcement.pinned = data["pinned"]
                announcement.updated_at = datetime.now()
                ret = Announcement_Schema().dump(announcement).data
                return (ret,200,headers)
            else:
                return (not_found,404,headers)

    def delete(self,announcement_id):
        """
        For DELETE request for specific id
        """
        user_status,user = has_admin_privileges()
        if user_status == "no_auth_token":
            return (bad_request,400,headers)

        if user_status == "not_logged_in":
            return (unauthorized,401,headers)

        if user_status == True:
            try:
                g.session.query(g.Base.classes.announcements).filter(g.Base.classes.announcements.id == announcement_id).delete()
                return ("",204,headers)
            except NoResultFound:
                return (not_found,404,headers)
            except:
                print(type(err))
                print(err)
                return (internal_server_error, 500, headers)
        else:
            return (forbidden,403,headers)
class Announcements_CR(Resource):
    """
    For GET PUT and DELETE for specific announcement
    """
    def get(self):
        """
        Getting all the announcements by hitting /announcements endpoint without any specific id
        """
        try:
            all_announcements = g.session.query(g.Base.classes.announcements).all()
            ret = Announcement_Schema(many = True).dump(all_announcements).data
            return (ret,200,headers)
        except:
            return (internal_server_error,500,headers)

    def post(self):
        """
        For POST request. Checks for bad JSON from request, checks if data types in request JSON are correct, Checks user auth status and if he's logged in.
        """
        try:
            data = request.get_json(force=True)
        except BadRequest:
            return (bad_request,400,headers)

        #data validation
        if Announcement_Schema().validate(data):
            return (unprocessable_entity,422,headers)

        #check if user has admin privileges
        user_status,user = has_admin_privileges()
        if user_status == "no_auth_token":
            return (bad_request,400,headers)

        if user_status == "not_logged_in":
            return (unauthorized,401,headers)

        if user_status == True:
            Announcements = g.Base.classes.announcements
            try:
                new_announcement = Announcements(
                                                    title = data["title"],
                                                    description = data["description"],
                                                    pinned = data["pinned"],
                                                    updated_at = datetime.now(),
                                                    created_at = datetime.now()
                                                )
                g.session.add(new_announcement)
                g.session.commit()
                ret = g.session.query(g.Base.classes.announcements).filter(g.Base.classes.announcements.description == data["description"]).one()
                ret = Announcement_Schema().dump(ret).data
                return (ret,201 ,headers)
            except Exception as err:
                print(type(err))
                print(err)
                return (internal_server_error,500,headers)
        else:
            return(forbidden,403,headers)
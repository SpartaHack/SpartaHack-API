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

    def delete(self,sponsor_id):
        user_status,user = has_admin_privileges()
        if user_status == "no_auth_token":
            return (bad_request,400,headers)

        if user_status == "not_logged_in":
            return (z,401,headers)

        if user_status in ["director","organizer"]:
            try:
                #this makes sure that at least one hardware matches hardware id
                sponsor_to_delete = g.session.query(g.Base.classes.sponsors).get(sponsor_id)
                if sponsor_to_delete:
                    g.session.query(g.Base.classes.sponsors).filter(g.Base.classes.sponsors.id == sponsor_id).delete()
                    return ("",204,headers)
                else:
                    return (not_found,404,headers)
            except Exception as err:
                print(type(err))
                print(err)
                return (internal_server_error,500,headers)
        else:
            return (forbidden,403,headers)

class Sponsor_CR(Resource):
    def post(self):
        """
        For POST request. Checks for bad JSON from request, checks if data types in request JSON are correct, Checks user auth status and if he's logged in.
        """
        try:
            data = request.get_json(force=True)
        except BadRequest:
            return (bad_request,400,headers)

        #data validation
        if Sponsor_Schema().validate(data):
            return (unprocessable_entity,422,headers)

        #check if user has admin privileges
        user_status,user = has_admin_privileges()
        if user_status == "no_auth_token":
            return (bad_request,400,headers)

        if user_status == "not_logged_in":
            return (unauthorized,401,headers)

        #checking if announcement with same title and description already exists. To manage duplicate entries
        try:
            exist_check = g.session.query(exists().where(and_(g.Base.classes.sponsors.name == data["name"],g.Base.classes.sponsors.url == data["url"]))).scalar()
            if exist_check:
                return (conflict,409,headers)
        except Exception as err:
            print(type(err))
            print(err)
            return (internal_server_error,500,headers)

        if user_status in ["director","organizer"]:
            Sponsors = g.Base.classes.sponsors
            try:
                new_sponsor = Sponsors(
                                        name = data["name"],
                                        url = data["url"],
                                        level = data["level"],
                                        logo_svg_light = data["logo_svg_light"],
                                        logo_png_light = data["logo_png_light"],
                                        updated_at = datetime.now(),
                                        created_at = datetime.now()
                                      )
                if data.get("logo_svg_dark"):
                    new_sponsor.logo_svg_dark = data["logo_svg_dark"]
                if data.get("logo_png_dark"):
                    new_sponsor.logo_png_dark = data["logo_png_dark"]

                g.session.add(new_sponsor)
                g.session.commit()
                ret = g.session.query(g.Base.classes.sponsors).filter(g.Base.classes.sponsors.name == data["name"]).one()
                return (Sponsor_Schema().dump(ret).data,201,headers)
            except Exception as err:
                print(type(err))
                print(err)
                return (internal_server_error,500,headers)
        else:
            return(forbidden,403,headers)

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
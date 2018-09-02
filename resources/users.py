from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from flask import request,jsonify,g
from marshmallow import validate,ValidationError
from sqlalchemy import exists,and_
from sqlalchemy.orm.exc import NoResultFound
from app import app
from common.json_schema import User_Schema,User_Input_Schema,User_Change_Role_Schema
from common.utils import headers,is_logged_in,has_admin_privileges
from common.utils import bad_request,unauthorized,forbidden,not_found,internal_server_error,unprocessable_entity,conflict
from datetime import datetime,timedelta
import string
import random
import secrets

class Users_RD(Resource):
    """
    For GET and DELETE for specific user_id
-    Director, Organizer should be able to get any user details and delete any user but not update
    """
    def get(self,user_id):
        """
        GET the user details based on specific user_id
        We are considering user and application separate entities. Previously, a user submitted the application details at the time of user account creation.
        Now, the user creates an account and then logs in to submit the application.
        Compared to old API we are not returning the application and rsvp details with the user details, rather we are returning the application_id and rsvp_id to help the front-end make GET request on application and rsvp endpoint in a separate requests.
        """
        #using get instead of query and it is marginally faster than filter
        #check for multiple entries need to be done at POST and not during GET or PUT or DELETE
        user_status,calling_user = has_admin_privileges()
        if user_status == "no_auth_token":
            return (bad_request,400,headers)

        if user_status == "not_logged_in":
            return (unauthorized,401,headers)

        # getting the user. Assuming the user exists. Case of user not existing is checked below
        try:
            user = g.session.query(g.Base.classes.users).get(user_id)
        except Exception as err:
            print(type(err))
            print(err)
            return (internal_server_error,500,headers)

        # *Only allow directors, organizers and the user making the request to access his own user id to access this resource
        # *Compare user_id rather than complete user objects because it's faster
        if user_status in ["director","organizer"] or calling_user.id == user.id:
            if user:
                ret = User_Schema().dump(user).data
                # *<class_name>_collection is way by which SQLAlchemy stores relationships.
                # *The collection object contains one related object in one-to-one relationship and more than one object in one-to-many relationships
                # *set application_id if application object is found in the applications_collection i.e. if the user has submitted the application
                # *This is different than old API in the sense that a user does not necessarily have a application at the time of account creation. User has the option of submitting the application later on.
                ret["application_id"] = user.applications_collection[0].id if len(user.applications_collection)>0 else None
                # *set rsvp_id if rsvp object is found in the rsvps_collection i.e. if the user has rsvped
                ret["rsvp_id"] = user.rsvps_collection[0].id if len(user.rsvps_collection)>0 else None
                return (ret,200,headers)
            else:
                return (not_found,404,headers)
        else:
            return(forbidden,403,headers)

    def delete(self,user_id):
        user_status,calling_user = has_admin_privileges()
        if user_status == "no_auth_token":
            return (bad_request,400,headers)

        if user_status == "not_logged_in":
            return (unauthorized,401,headers)

        # getting the user. Assuming the user exists. Case of user not existing is checked below
        try:
            user = g.session.query(g.Base.classes.users).get(user_id)
        except Exception as err:
            print(type(err))
            print(err)
            return (internal_server_error,500,headers)

        if user_status in ["director","organizer"] or calling_user.id == user.id:
            try:
                if user:
                    if len(user.rsvps_collection)>0:
                        g.session.delete(g.session.query(g.Base.classes.rsvps).get(user.rsvps_collection[0].id))
                    if len(user.applications_collection)>0:
                        g.session.delete(g.session.query(g.Base.classes.applications).get(user.applications_collection[0].id))
                    g.session.delete(g.session.query(g.Base.classes.users).get(user_id))
                    return ("",204,headers)
                else:
                    return (not_found,404,headers)
            except Exception as err:
                print(type(err))
                print(err)
                return (internal_server_error, 500, headers)
        else:
            return (forbidden,403,headers)

class Users_CRU(Resource):
    """
    To create new user using POST and read all users
    """
    def put(self):
        """
        Update user. Required data: email, first_name, last_name, password, confirmation_password
        PUT is allowed only by users on their own objects.
        """
        user_status,calling_user = has_admin_privileges()
        if user_status == "no_auth_token":
            return (bad_request,400,headers)
        if user_status == "not_logged_in":
            return (unauthorized,401,headers)

        #check if data from request is serializable
        try:
            data = request.get_json(force=True)
        except BadRequest:
            return (bad_request,400,headers)

        # *request data validation. Check for empty fields will be done by frontend
        validation = User_Input_Schema().validate(data)
        if validation:
            unprocessable_entity["error_list"] = validation["_schema"]
            return (unprocessable_entity,422,headers)

        # *Only allow user making the request to access his own user id to access this resource
        # *The original email, first_name and last_name to be provided in the request. Just updated value setting will be implemented in PATCH which would be in API 2.0
        try:
            calling_user.email = data["email"]
            calling_user.first_name = data["first_name"]
            calling_user.last_name = data["last_name"]
            # *Update password only if password is given
            if data.get("password"):
                calling_user.encrypted_password = app.config["CRYPTO_CONTEXT"].hash(data["password"])

            return (User_Schema().dump(calling_user).data,200,headers)
        except Exception as err:
            print(type(err))
            print(err)
            return (internal_server_error,500,headers)

    def post(self):
        """
        Create new user. Required data: email,password,confirmation_password,first_name,last_name
        """
        Users = g.Base.classes.users
        try:
            data = request.get_json(force=True)
        except BadRequest:
            return (bad_request,400,headers)

        # *request data validation. Check for empty fields will be done by frontend
        validation = User_Input_Schema().validate(data)
        if validation:
            unprocessable_entity["error_list"]=validation["_schema"]
            return (unprocessable_entity,422,headers)

        # check if user already signed up
        try:
            exist_check = g.session.query(exists().where(Users.email == data["email"])).scalar()
            if exist_check:
                print(exist_check)
                app.config["CRYPTO_CONTEXT"].dummy_verify()
                return (conflict,409,headers)
        except Exception as err:
            print(type(err))
            print(err)
            return (internal_server_error,500,headers)

        #* Encrypt password
        encrypted_pass = app.config["CRYPTO_CONTEXT"].hash(data["password"])

        try:
            new_user = Users(
                                email = data["email"],
                                encrypted_password = encrypted_pass,
                                sign_in_count = 0,
                                checked_in = False,
                                role = 64,
                                auth_token = secrets.token_urlsafe(25),
                                first_name = data["first_name"],
                                last_name = data["last_name"],
                                confirmation_token = secrets.token_urlsafe(15),
                                confirmation_sent_at = datetime.now(),
                                updated_at = datetime.now(),
                                created_at = datetime.now()
                            )
            g.session.add(new_user)
            g.session.commit()
            ret = g.session.query(Users).filter(Users.encrypted_password == encrypted_pass).one()
            return (User_Schema().dump(ret).data,201 ,headers)
        except Exception as err:
            print(type(err))
            print(err)
            return (internal_server_error,500,headers)

    def get(self):
        """
        GET all the users at a time.
        Application_id and rsvp_id is not gonna be returned when GET is called on all the users.
        Because getting the application_id and rsvp_id makes db calls and making calls for application_id and rsvp_id on hundreds of users is costly.
        """
        user_status,calling_user = has_admin_privileges()
        if user_status == "no_auth_token":
            return (bad_request,400,headers)

        if user_status == "not_logged_in":
            return (unauthorized,401,headers)

        # *Only allow directors, organizers to make GET on all users (I don't really see the need for this tbh!)maybe for accepting applications
        if user_status in ["director","organizer"]:
            try:
                all_users = g.session.query(g.Base.classes.users).all()
                ret = User_Schema(many = True).dump(all_users).data
                return (ret,200,headers)
            except Exception as err:
                print(type(err))
                print(err)
                return (internal_server_error,500,headers)
        else:
            return(forbidden,403,headers)

class Users_Change_Role(Resource):
    """
    Update roles for users. Required data: email,role, role_change_password
    """
    def post(self):
        """
        Only method needed
        """
        user_status,calling_user = has_admin_privileges()
        print(user_status)
        if user_status == "no_auth_token":
            return (bad_request,400,headers)

        if user_status == "not_logged_in":
            return (unauthorized,401,headers)

        try:
            data = request.get_json(force=True)
        except BadRequest:
            return (bad_request,400,headers)

        # *request data validation
        validation = User_Change_Role_Schema().validate(data)
        if validation:
            unprocessable_entity["error_list"] = validation["_schema"]
            return (unprocessable_entity,422,headers)

        # getting the user. Assuming the user exists. Case of user not existing is checked below
        try:
            user = g.session.query(g.Base.classes.users).filter(g.Base.classes.users.email == data["email"]).one()
        except Exception as err:
            print(type(err))
            print(err)
            return (internal_server_error,500,headers)

        # *Only directors have the ability to change user roles
        try:
            if user_status in ["director"] and data["role_change_password"] == app.config["ROLE_CHANGE_PASS_DEV"]:
                if user:
                    user.role = 2**(["director","judge","mentor","sponsor","organizer","volunteer","hacker"].index(data["role"]))
                    return (User_Schema().dump(user).data,200,headers)
                else:
                    return (not_found,404,headers)
            else:
                return (forbidden,403,headers)
        except Exception as err:
            print(type(err))
            print(err)
            return (internal_server_error,500,headers)

class Users_Request_Password_Token(Resource):
    """
    Create password reset token
    """
    def post(self):
        pass
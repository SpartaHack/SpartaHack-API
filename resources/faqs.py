from flask_restful import Resource
from flask import request,jsonify
from  sqlalchemy.orm.exc import NoResultFound
from models.faqs import Faqs
from models.users import Users

def is_logged_in():
    user_token=request.headers.get("X-WWW-USER-TOKEN")
    try:
        user=Users.query.filter(Users.__table__.c.auth_token==user_token).one()
        return user
    except:
        return False

def has_admin_privileges():
    user=is_logged_in()
    if user:
        if user.role<9:
            return True
        else:
            return False
    else:
        return "Not logged in"
class Faqs_RUD(Resource):
    """
    For GET PUT and DELETE for specific faq
    get http headers using request.headers.get("header_name")
    """
    def get(self,faq_id):
        try:
            faq_object=Faqs.query.filter(Faqs.__table__.c.id == faq_id).one()
            ret={
                    "id":faq_object.id,
                    "priority":faq_object.priority,
                    "display":faq_object.display,
                    "question":faq_object.question,
                    "answer":faq_object.answer,
                    "placement":faq_object.placement,
                    "user":faq_object.user_id
                }
            return jsonify(ret)

        except NoResultFound:
            return jsonify({"status":404,"error":"Not Found"})


    def put(self,faq_id):
        user_status=has_admin_privileges()
        if user_status=="Not logged in":
            if user_status==True:
                try:
                    faq_object=Faqs.query.get(faq_id)
                    return faq_object.id
                except:
                    return "Something failed"
            else:
                return "Not authenticated"
        else:
            return "Not logged in"


    def delete(self,faq_id):
        pass

class Faqs_CR(Resource):
    """
    For adding a new faq through POST and getting all the FAQS
    """
    def post(self):
        pass

    def get(self):
        return "FAQS_CR"
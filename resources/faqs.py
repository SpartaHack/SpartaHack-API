from flask_restful import Resource
from flask import request,jsonify,Response
from sqlalchemy.orm.exc import NoResultFound
from common.utils import error,headers,is_logged_in,has_admin_privileges
from models.faqs import Faqs

class Faqs_RUD(Resource):
    """
    For GET PUT and DELETE for specific faq
    get http headers using request.headers.get("header_name")
    """
    def get(self,faq_id):
        try:
            faq_object = Faqs.query.filter(Faqs.__table__.c.id == faq_id).one()
            ret={
                    "id":faq_object.id,
                    "priority":faq_object.priority,
                    "display":faq_object.display,
                    "question":faq_object.question,
                    "answer":faq_object.answer,
                    "placement":faq_object.placement,
                    "user":faq_object.user_id
                }
            return (ret,200,headers)

        except NoResultFound:
            return (error,404,headers)


    def put(self,faq_id):
        user_statu = has_admin_privileges()
        if user_status == "Not logged in":
            if user_status == True:
                try:
                    faq_object = Faqs.query.get(faq_id)
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
        return ({"F":"gd"},200,{"X-XSS-Protection":"1"})
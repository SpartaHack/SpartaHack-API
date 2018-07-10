from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from flask import request,jsonify,g
from sqlalchemy.orm.exc import NoResultFound
from common.utils import headers,is_logged_in,has_admin_privileges
from common.utils import bad_request,unauthorised,forbidden,not_found,internal_server_error

class Faqs_RUD(Resource):
    """
    For GET PUT and DELETE for specific faq
    get http headers using request.headers.get("header_name")
    """
    def get(self,faq_id):
        try:
            faq_object = g.session.query(g.Base.classes.faqs).filter(g.Base.classes.faqs.id == faq_id).one()
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
            return (not_found,404,headers)


    def put(self,faq_id):
        try:
            data=request.get_json(force=True)
        except BadRequest:
            return (bad_request,400,headers)

        user_status = has_admin_privileges()
        if user_status == "no_header_found":
            return (bad_request,400,headers)

        if user_status == "not_logged_in":
            return (unauthorised,401,headers)

        if user_status == True:
            try:
                faq_object = Faqs.query.get(faq_id)
                return faq_object.id
            except:
                return "Something failed"
        else:
            return (unauthorised,401,headers)



    def delete(self,faq_id):
        pass

class Faqs_CR(Resource):
    """
    For adding a new faq through POST and getting all the FAQS
    """
    def post(self):
        pass

    def get(self):
        try:
            all_faqs=g.session.query(g.Base.classes.faqs).all()
            ret=[]
            for faq in all_faqs:
                ret.append(
                            {
                            "id":faq.id,
                            "priority":faq.priority,
                            "display":faq.display,
                            "question":faq.question,
                            "answer":faq.answer,
                            "placement":faq.placement,
                            "user":faq.user_id
                            }
                          )
            return (ret,200,headers)
        except:
            return (internal_server_error,500,headers)
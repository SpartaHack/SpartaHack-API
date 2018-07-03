from flask_restful import Resource
from flask import request
from models.faqs import Faqs
from models.users import Users

def faq_exists(faq_id):
    faq=Faqs()
    pass


def has_admin_privileges():
    user_token=request.headers.get("X-WWW-USER-TOKEN")
    return user_token
class Faqs_RUD(Resource):
    """
    For GET PUT and DELETE for specific faq
    get http headers using request.headers.get("header_name")
    """
    def get(self,faq_id):
        if faq_exists(faq_id):
            pass
        else:
            return "Nope"

        return {"question":"This is amazzzing!"}

    def put(self,faq_id):
        if has_admin_privileges():
            if faq_exists(faq_id):
                pass
            else:
                return "Nope"
        else:
            return "Not authenticated"


    def delete(self,faq_id):
        pass

class Faqs_CR(Resource):
    """
    For adding a new faq through POST and getting all the FAQS
    """
    def post(self):
        pass

    def get(self):
        pass
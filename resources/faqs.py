from flask_restful import Resource
from flask import request

def abort_if_faq_doesnt_exist(faq_id):
    pass

class Faqs_RUD(Resource):
    """
    For GET PUT and DELETE for specific faq
    get http headers using request.headers.get("header_name")
    """
    def get(self,faq_id):
        abort_if_faq_doesnt_exist(faq_id)
        return {"question":"This is amazzzing!"}

    def put(self,faq_id):
        pass

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
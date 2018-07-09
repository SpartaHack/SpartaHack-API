from flask import request
from models.users import Users

error={"status":404,"error":"Not Found"}

headers={
            "X-XSS-Protection":"1",
            "X-Frame-Options": "sameorigin",
            "Connection" : "keep-alive",
            "X-Content-Type-Options": "nosniff"
        }

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
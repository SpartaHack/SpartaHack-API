from flask import request,g
import math

bad_request = {"status":400,"message":"Bad Request"}
unauthorized = {"status":401,"message":"Unauthorized"}
forbidden = {"status":403,"message":"Forbidden"}
not_found = {"status":404,"message":"Not Found"}
unprocessable_entity = {"status":422,"message":"Unprocessable Entity","error_list":{}}
internal_server_error = {"status":500,"message":"Internal Server Error"}
conflict = {"status":409,"message":"Conflict"}

headers = {
            "X-XSS-Protection" : "1; mode=block",
            "X-Frame-Options" : "DENY",
            "Connection" : "keep-alive",
            "X-Content-Type-Options" : "nosniff",
            "Cache-Control" : "max-age=0, private, must-revalidate"
        }

def is_logged_in():
    user_token=request.headers.get("X-WWW-USER-TOKEN",default=False)
    if user_token:
        try:
            user=g.session.query(g.Base.classes.users).filter(g.Base.classes.users.auth_token == user_token).one()
            return user
        except Exception as err:
            print(type(err))
            print(err)
            return False
    else:
        return("no_auth_token")


def has_admin_privileges():
    user = is_logged_in()
    if user == "no_auth_token":
        return "no_auth_token",user
    roles = ["director","judge","mentor","sponsor","organizer","volunteer","hacker"]
    if user:
        return roles[int(math.log(int(user.role),2))],user
    else:
        return "not_logged_in",user

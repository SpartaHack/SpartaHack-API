from flask import request,g

bad_request = {"status":400,"error":"Bad Request"}
unauthorised = {"status":401,"error":"Unauthorised"}
forbidden = {"status":403,"error":"Forbidden"}
not_found = {"status":404,"error":"Not Found"}
unprocessable_entity = {"status":422,"error":"Unprocessable Entity"}
internal_server_error = {"status":500,"error":"Internal Server Error"}

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
        except:
            return False
    else:
        return("no_auth_token")


def has_admin_privileges():
    user = is_logged_in()
    if user == "no_auth_token":
        return "no_auth_token",user
    if user:
        if user.role < 9:
            return True,user
        else:
            return False,user
    else:
        return "not_logged_in",user
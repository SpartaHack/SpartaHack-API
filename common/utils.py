from flask import request,g
import math
from flask import current_app as app
import smtplib
from email.message import EmailMessage
from six.moves.urllib.request import urlopen
from jose import jwt
import os
import json

bad_request = {"status":400,"message":"Bad Request","error_list":{}}
unauthorized = {"status":401,"message":"Unauthorized","error_list":{}}
forbidden = {"status":403,"message":"Forbidden","error_list":{}}
not_found = {"status":404,"message":"Not Found","error_list":{}}
unprocessable_entity = {"status":422,"message":"Unprocessable Entity","error_list":{}}
internal_server_error = {"status":500,"message":"Internal Server Error","error_list":{}}
conflict = {"status":409,"message":"Conflict","error_list":{}}
gone = {"status":410,"message":"Gone","error_list":{}}

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
    role = ["director","judge","mentor","sponsor","organizer","volunteer","hacker"]
    if user:
        return role[int(math.log(int(user.role),2))],user
    else:
        return "not_logged_in",user

def encrypt_pass(password):
    return app.config["CRYPTO_CONTEXT"].hash(password)

def waste_time():
    app.config["CRYPTO_CONTEXT"].dummy_verify()

def verify_pass(password,password_hash):
    return app.config["CRYPTO_CONTEXT"].verify(password,hash = password_hash)

def send_email(subject,recipient,body):
    try:
        #creating SMTP server connection
        mail_server = smtplib.SMTP(host=app.config["MAIL_SERVER"], port=app.config["MAIL_PORT"])
        mail_server.starttls()
        mail_server.login(app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])

        #creating email
        msg = EmailMessage()
        msg['From'] = app.config["MAIL_USERNAME"]
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.set_content(body,subtype = 'html')

        #sending email
        mail_server.send_message(msg)
    except smtplib.SMTPException as error:
        print (str(error))
        print ("Error: unable to send email")
    finally:
        mail_server.quit()


def get_access_token():
    access_token = (request.headers.get("Authorization"))
    access_token = access_token.split()
    return access_token[1][6:]

def validate_ID_Token(id_token):
    parts = id_token.split(".")

    #check if JWT is correctly formatted
    if (len(parts) != 3):
        return False

    jsonurl = urlopen("""https://"""+os.getenv("AUTH0_DOMAIN")+"""/.well-known/jwks.json""")
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(id_token)

    # Get correct RSA key for the token
    rsa_key = {}
    for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }

    # Extract access token from the request
    access_token = get_access_token()

    # Decoded the token based on the RSA key
    if rsa_key:
        try:
            payload = jwt.decode(
                id_token,
                rsa_key,
                algorithms=os.getenv("ALGORITHMS"),
                audience=os.getenv("API_AUDIENCE"),
                issuer="https://"+os.getenv("AUTH0_DOMAIN")+"/",
                access_token=access_token
            )
        except Exception as err:
            print(type(err))
            print(err)
            return False

    return payload

def verify_id_token(id_token):
    if (id_token == os.getenv("ID_Token")):
        return True
    else:
        return False
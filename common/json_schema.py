from marshmallow import Schema,fields,ValidationError,validates_schema,validate
import ipaddress
import math
import string

"""
schema.dump = used for converting the automap.faqs object to a dictionary good for returning ie cleaning unnecessary fields
schema.validate(request.get_json(force=True)) = used to validate if all the data required for updating and creating the faq is present.4
dump_only = Fields that we need to display when returning the item
load_only = Fields that we need only while dumping from python objects. We use it to stop marshmallow from dumping it while using dump()
"""
def ip_test(obj):
    try:
        ipaddress.ip_address(obj)
        return True
    except ValueError:
        return False

def password_check(obj):
        if obj.password == obj.password_confirmation:
            return 

class Faq_Schema(Schema):
    id = fields.Integer()
    question = fields.String(required=True)
    answer = fields.String(required=True)
    display = fields.Boolean(required=True)
    priority = fields.Integer(required=True)
    placement = fields.String(required=True)
    user_id = fields.Integer()

class Announcement_Schema(Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    description = fields.String(required=True)
    pinned = fields.Boolean(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class Hardware_Schema(Schema):
    id = fields.Integer()
    item = fields.String(required=True)
    lender = fields.String(required=True)
    quantity = fields.String(required=True)
    created_at = fields.DateTime(load_only=True)
    updated_at = fields.DateTime(load_only=True)

class Sponsor_Schema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    level = fields.String(required=True)
    url = fields.URL(required=True)
    logo_svg_light = fields.String(required=True)
    logo_svg_dark = fields.String()
    logo_png_light = fields.String(required=True)
    logo_png_dark = fields.String()
    created_at = fields.DateTime(load_only=True)
    updated_at = fields.DateTime(load_only=True)

class Schedule_Schema(Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    description = fields.String(required=True)
    time = fields.DateTime(required=True)
    location = fields.String(required=True)
    created_at = fields.DateTime(load_only=True)
    updated_at = fields.DateTime(dump_only=True)

class Application_Schema(Schema):
    id = fields.Integer()
    user_id = fields.Integer(required=True  )
    birth_day = fields.Integer(required=True)
    birth_month = fields.Integer(required=True)
    birth_year = fields.Integer(required=True)
    education = fields.String(required=True)
    university = fields.String()
    other_university = fields.String()
    travel_origin = fields.String()
    graduation_season = fields.String(required=True)
    graduation_year = fields.Integer(required=True)
    major = fields.List(fields.String)
    hackathons = fields.Integer(required=True)
    github = fields.URL()
    linkedin = fields.URL()
    website = fields.URL()
    devpost = fields.URL()
    other_link = fields.URL()
    statement = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    race = fields.List(fields.String)
    gender = fields.String()
    outside_north_america = fields.String()
    status = fields.String()
    accepted_date = fields.DateTime()

class User_Schema(Schema):
    def role_convert(self,obj):
        roles = ["director","judge","mentor","sponsor","organizer","volunteer","hacker"]
        return roles[int(math.log(int(obj.role),2))]

    id = fields.Integer(dump_only=True)
    email = fields.Email(dump_only=True,required=True)
    encrypted_password = fields.String()
    reset_password_token = fields.String(dump_only=True)
    reset_password_sent_at = fields.DateTime()
    remember_created_at = fields.DateTime()
    sign_in_count = fields.Integer()
    current_sign_in_at = fields.DateTime()
    last_sign_in_at = fields.DateTime()
    current_sign_in_ip = fields.String(validate=ip_test)
    last_sign_in_ip = fields.String(validate=ip_test)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    auth_token =fields.String(dump_only=True)
    confirmation_token = fields.String()
    confirmed_at = fields.DateTime()
    confirmation_sent_at = fields.DateTime()
    role = fields.Method("role_convert")
    first_name = fields.String(dump_only=True)
    last_name = fields.String(dump_only=True)
    checked_in = fields.Boolean(dump_only=True)

class User_Input_Schema(Schema):
    email = fields.String()
    password = fields.String()
    confirm_password = fields.String()
    first_name = fields.String()
    last_name = fields.String()

    @validates_schema
    def check_all_fields(self,data):

        errors={}
        try:
            validator = validate.Email()
            validator(data["email"])
        except ValidationError:
            errors["email"] = "Not an valid email!"

        if data.get("password") and data.get("password") and data["password"] != data["confirm_password"]:
            errors["confirm_password"] = "Passsword and Confirm password don't match"

        # *might not need it
        # if data["roles"] not in ["director","judge","mentor","sponsor","organizer","volunteer","hacker"]:
        #     errors["roles"] = "Not a valid role"

        #checking if first and last name have any special characters or numbers
        if any(char in string.punctuation for char in data["first_name"]) or any(char in string.digits for char in data["first_name"]):
            errors["first_name"] = "Not a valid first name"

        if any(char in string.punctuation for char in data["last_name"]) or any(char in string.digits for char in data["last_name"]):
            errors["last_name"] = "Not a valid last name"

        if errors:
            raise ValidationError(errors)

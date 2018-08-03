from marshmallow import Schema,fields

"""
    schema.dump = used for converting the automap.faqs object to a dictionary good for returning ie cleaning unnecessary fields
    schema.validate(request.get_json(force=True)) = used to validate if all the data required for updating and creating the faq is present.4
    dump_only = Fields that we need to display when returning the item
    load_only = Fields that we need only while dumping from python objects. We use it to stop marshmallow from dumping it while using dump()
"""


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

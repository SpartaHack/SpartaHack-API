from marshmallow import Schema,fields

class Faq_Schema(Schema):
    """
    schema.dump = used for converting the automap.faqs object to a dictionary good for returning ie cleaning unncessary fields
    schema.validate(request.get_json(force=True)) = used to validate if all the data required for updating and creating the faq is present.
    """
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
from marshmallow import Schema,fields

class Faq_Schema(Schema):
    """
    schema.dump = used for converting the automap.faqs object to a dictionary good for returning ie cleaning unncessary fields
    schema.validate(request.get_json(force=True)) = used to validate if all the data required for updating and creating the faq is present.
    """
    id = fields.String(dump_only=True)
    question = fields.String(dump_only=True,required=True)
    answer = fields.String(dump_only=True,required=True)
    display = fields.Boolean(dump_only=True,required=True)
    priority = fields.Integer(dump_only=True,required=True)
    placement = fields.String(dump_only=True,required=True)
    user_id = fields.Integer(dump_only=True)
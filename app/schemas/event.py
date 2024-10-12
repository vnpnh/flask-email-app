from marshmallow import Schema, fields

class EventSchema(Schema):
    event_name = fields.Str(required=True, validate=lambda s: len(s) > 0)
    event_description = fields.Str()
    event_date = fields.DateTime(required=True)

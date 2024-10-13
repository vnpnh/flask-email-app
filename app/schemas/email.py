from marshmallow import Schema, ValidationError, fields, validates

from app.database import db
from app.models.event import Event


class EmailSchema(Schema):
    event_id = fields.Int(required=True, validate=lambda val: val > 0)
    email_subject = fields.Str(required=True, validate=lambda s: len(s) >= 5 and len(s) <= 255)
    email_content = fields.Str(required=True, validate=lambda s: len(s) <= 5000)
    scheduled_at = fields.DateTime(required=True, format='%Y-%m-%dT%H:%M:%SZ')

    status = fields.Str(missing="scheduled")

    @validates('event_id')
    def validate_event_id(self, value):
        """Validate if the event_id exists in the database."""
        event = db.session.get(Event, value)
        if not event:
            raise ValidationError(f"Event with id {value} does not exist.")

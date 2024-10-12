from marshmallow import Schema, fields, validates_schema, ValidationError, validates
from app.models.recipient import Recipient
from app.models.event import Event
from app.models.user import User


class RecipientSchema(Schema):
    user_id = fields.List(fields.Int(), required=True)
    event_id = fields.Int(required=True)

    @validates_schema
    def validate_unique_recipients(self, data, **kwargs):
        """Ensure the (user_id, event_id) combination is unique for each user."""
        user_ids = data.get('user_id', [])
        event_id = data.get('event_id')

        if len(user_ids) != len(set(user_ids)):
            raise ValidationError("Duplicate user IDs found in the list.", field_name="user_id")

        event = Event.query.get(event_id)
        if not event:
            raise ValidationError(f"Event with id {event_id} does not exist.", field_name='event_id')

        errors = {}
        for user_id in user_ids:
            user = User.query.get(user_id)
            if not user:
                errors[f"user_id {user_id}"] = f"User with id {user_id} does not exist."

            recipient = Recipient.query.filter_by(user_id=user_id, event_id=event_id).first()
            if recipient:
                errors[f"user_id {user_id}"] = (
                    f"Recipient with user_id {user_id} and event_id {event_id} already exists."
                )

        if errors:
            raise ValidationError(errors)

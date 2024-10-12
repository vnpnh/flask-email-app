from marshmallow import Schema, fields, validates, ValidationError

from app.models.user import User


class UserSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email_address = fields.Email(required=True)

    @validates('email_address')
    def validate_unique_email(self, value):
        """Check if the email address is already taken."""
        if User.query.filter_by(email_address=value).first():
            raise ValidationError(f"The email address '{value}' is already in use.")

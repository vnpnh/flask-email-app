from app.database import db
from app.models.base import BaseModel


class Event(BaseModel):
    __tablename__ = 'event'

    event_name = db.Column(db.String(255), nullable=False)
    event_description = db.Column(db.Text, nullable=True)
    event_date = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'event_id': self.event_id,
            'event_name': self.event_name,
            'event_description': self.event_description,
            'event_date': self.event_date,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

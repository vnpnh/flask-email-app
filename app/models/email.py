from ..database import db
from .base import BaseModel


class Email(BaseModel):
    __tablename__ = 'email'

    event_id = db.Column(db.Integer, nullable=False, index=True)
    email_subject = db.Column(db.String(255, collation='utf8mb4_unicode_ci'), nullable=False)
    email_content = db.Column(db.Text(collation='utf8mb4_unicode_ci'), nullable=False)
    scheduled_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="scheduled", nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'email_subject': self.email_subject,
            'email_content': self.email_content,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'status': self.status
        }

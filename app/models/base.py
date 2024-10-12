from datetime import datetime, timezone

from app.database import db


class BaseModel(db.Model):
    """ Base Model class """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def save(self):
        """ Save a model instance """
        db.session.add(self)
        db.session.commit()

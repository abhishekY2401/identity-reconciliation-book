from datetime import datetime, timezone
from app.database import db


class Contact(db.Model):
    '''Contact Details

    '''
    __tablename__ = 'contact'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    linked_id = db.Column(db.Integer, db.ForeignKey(
        'contact.id'), nullable=True)
    link_precedence = db.Column(
        db.Enum('primary', 'secondary', name='link_precedence_enum'), nullable=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(
        timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(
        timezone.utc), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Contact {self.id} - {self.email} - {self.phone_number}>'

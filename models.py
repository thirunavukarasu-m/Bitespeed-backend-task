from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    phoneNumber = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    
    linkedId = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=True)
    
    linkPrecedence = db.Column(db.Enum('primary', 'secondary', name='link_precedence'), nullable=False, default='primary')
    
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deletedAt = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Contact id={self.id} email={self.email} phone={self.phoneNumber} linkedId={self.linkedId}>"

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Message(db.Model, SerializerMixin):
    """
    Model representing a message in the system.

    Attributes:
        id (int): Primary key of the message.
        body (str): Content of the message.
        username (str): Username associated with the message.
        created_at (datetime): Timestamp when the message was created.
        updated_at (datetime): Timestamp when the message was last updated.
    """
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'<Message id={self.id}, by {self.username}: "{self.body[:20]}...">'

    # Optional: Add custom validation methods if needed
    # def validate_body(self, value):
    #     if not value:
    #         raise ValueError("Body must not be empty.")

# Example usage:
# To use this model, ensure you have SQLAlchemy configured with your Flask app,
# and manage migrations accordingly.

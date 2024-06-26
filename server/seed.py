#!/usr/bin/env python3

from random import choice as rc
from faker import Faker
from app import app
from models import db, Message

fake = Faker()

usernames = [fake.first_name() for i in range(4)]
if "Duane" not in usernames:
    usernames.append("Duane")

def delete_messages():
    """Delete all existing messages from the database."""
    Message.query.delete()

def generate_messages(num_messages=20):
    """Generate and return a list of fake Message objects."""
    messages = []
    for _ in range(num_messages):
        message = Message(
            body=fake.sentence(),
            username=rc(usernames),
        )
        messages.append(message)
    return messages

def save_messages(messages):
    """Save a list of Message objects to the database."""
    db.session.add_all(messages)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        delete_messages()
        messages_to_save = generate_messages()
        save_messages(messages_to_save)

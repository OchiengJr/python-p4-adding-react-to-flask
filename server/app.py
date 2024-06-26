from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_encoder = CustomJSONEncoder  # Optional: Implement a custom JSON encoder if needed

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle datetime serialization."""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        try:
            messages = Message.query.order_by(Message.created_at).all()
            response_data = [message.to_dict() for message in messages]
            status_code = 200
        except SQLAlchemyError as e:
            response_data = {'error': str(e)}
            status_code = 500
        
        return jsonify(response_data), status_code
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            message = Message(body=data['body'], username=data['username'])
            db.session.add(message)
            db.session.commit()
            response_data = message.to_dict()
            status_code = 201
        except KeyError as e:
            response_data = {'error': f'Missing required field: {str(e)}'}
            status_code = 400
        except SQLAlchemyError as e:
            db.session.rollback()
            response_data = {'error': str(e)}
            status_code = 500
        
        return jsonify(response_data), status_code

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.get(id)

    if not message:
        return jsonify({'error': 'Message not found'}), 404

    if request.method == 'PATCH':
        try:
            data = request.get_json()
            for attr, value in data.items():
                setattr(message, attr, value)
            db.session.commit()
            response_data = message.to_dict()
            status_code = 200
        except SQLAlchemyError as e:
            db.session.rollback()
            response_data = {'error': str(e)}
            status_code = 500
        
        return jsonify(response_data), status_code

    elif request.method == 'DELETE':
        try:
            db.session.delete(message)
            db.session.commit()
            response_data = {'deleted': True}
            status_code = 200
        except SQLAlchemyError as e:
            db.session.rollback()
            response_data = {'error': str(e)}
            status_code = 500
        
        return jsonify(response_data), status_code

if __name__ == "__main__":
    app.run(port=5555, debug=True)

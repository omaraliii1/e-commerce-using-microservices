from flask import Flask, jsonify, request, current_app, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token ,jwt_required, get_jwt_identity, get_jwt, JWTManager
from models import User
from extensions import db
import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db.init_app(app)
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if data:
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({'message': 'Email already exists.', "status": "failed"})
        elif len(email) < 4:
            return jsonify({'message': 'Email must be greater than 3 characters', "status": "failed"})
        elif len(username) < 2:
            return jsonify({'message': 'Username must be greater than 1 character.', "status": "failed"})
        elif len(password) < 7:
            return jsonify({'message': 'Password must be at least 7 characters.', "status": "failed"})
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha1'))
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'Account created!', 'user_id': new_user.id, "status": "success"})
    else:
        return jsonify({'message': 'Invalid request.', "status": "failed"})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data:
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)  
            return jsonify({'message': 'Logged in successfully!', 'access_token': access_token, "status": "success"})
        else:
            return jsonify({'message': 'Incorrect username or password.', "status": "failed"})
    else:
        return jsonify({'message': 'Invalid request.', "status": "failed"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
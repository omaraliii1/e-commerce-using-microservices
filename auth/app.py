from flask import Flask, jsonify, request, current_app, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token ,jwt_required, get_jwt_identity, get_jwt, JWTManager
from models import User
from extensions import db
from os import environ

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@192.168.49.2:30002/cloud'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')

app.config['SECRET_KEY'] = 'test123'
app.config['JWT_SECRET_KEY'] = 'test123'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


db.init_app(app)
jwt = JWTManager(app)

def check_for_schema_changes():
    with app.app_context():
        inspector = db.inspect(db.engine)
        existing_tables = inspector.get_table_names()
        declared_tables = db.metadata.tables.keys()

        for table_name in declared_tables:
            if table_name not in existing_tables:
                db.create_all()
                print(f"Table '{table_name}' created.")

check_for_schema_changes()


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
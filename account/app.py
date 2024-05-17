from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, JWTManager
from models import User, Cart
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

BLACKLIST = set()


@jwt.token_in_blocklist_loader
def is_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in BLACKLIST

@app.route('/', methods=['GET'])
@jwt_required()
def main():
    current_user = get_jwt_identity()
    if current_user:
        return jsonify({'message': 'User authenticated', 'user': current_user}), 200
    else:
        return jsonify({'message': 'User not authenticated', 'status': 'failed'})

@app.route('/cart', methods=['GET'])
@jwt_required()
def cart():
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({'message': 'User not authenticated', 'status': 'failed'}), 401
    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({'message': 'User not found', 'status': 'failed'}), 404
    cart_items = current_user.carts 
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    return jsonify({'cart_items': [item.serialize() for item in cart_items], 'subtotal': subtotal, 'status': 'success'}), 200

@app.route('/cart/remove/<int:id>', methods=['GET'])
@jwt_required()
def remove_from_cart(id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user:
        return jsonify({'message': 'User not found', 'status': 'failed'}), 404
    
    cart_item = Cart.query.filter_by(product_id=id, user_id=current_user_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        
        cart_items = Cart.query.filter_by(user_id=current_user_id).all()
        if cart_items:
            subtotal = sum(item.product.price * item.quantity for item in cart_items)
            return jsonify({'cart_items': [item.serialize() for item in cart_items], 'subtotal': subtotal, 'status': 'success'})
        else:
            return jsonify({'message': 'Your cart is empty.', 'status': 'success'})
    else:
        return jsonify({'message': 'Item not found in your cart.', 'status': 'failed'})

@app.route('/change_address', methods=['POST'])
@jwt_required()
def change_address():
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({'message': 'User not authenticated', 'status': 'failed'})
    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({'message': 'User not found', 'status': 'failed'})
    address = request.json.get('address')
    current_user.address = address
    db.session.commit()
    return jsonify({'message': 'Address changed successfully!', 'status': 'success'}), 200

@app.route('/change_password', methods=['POST'])
@jwt_required()
def change_password():
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({'message': 'User not authenticated', 'status': 'failed'})
    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({'message': 'User not found', 'status': 'failed'})
    password = request.json.get('password')
    new_password = request.json.get('new_password')
    confirm_password = request.json.get('confirm_password')
    if check_password_hash(current_user.password, password):
        if new_password == confirm_password:
            current_user.password = generate_password_hash(new_password, method='pbkdf2:sha1')
            db.session.commit()
            jti = get_jwt()['jti']
            BLACKLIST.add(jti)
            return jsonify({'message': 'Password changed successfully!', 'status': 'success'}), 200
        else:
            return jsonify({'message': 'Passwords do not match!', 'status': 'failed'}), 400
    else:
        return jsonify({'message': 'Incorrect password!', 'status': 'failed'}), 400

@app.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_account():
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({'message': 'User not authenticated', 'status': 'failed'}), 401
    
    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({'message': 'User not found', 'status': 'failed'}), 404
    
    db.session.delete(current_user)
    db.session.commit()
    
    return jsonify({'message': 'Account deleted successfully!', 'status': 'success'}), 200

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    BLACKLIST.add(jti)
    return jsonify({'message': 'Successfully logged out'}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

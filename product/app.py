from extensions import db
from flask import Flask, jsonify, request
from models import Product, Cart,User
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db.init_app(app)
jwt = JWTManager(app)

@app.route('/products', methods=['GET'])
def products():
    if request.method == 'GET':
        products = Product.query.all()
        return jsonify({'products': [product.serialize() for product in products]})
    return jsonify({'message': 'Invalid request.', 'status': 'failed'})

@app.route('/products/<int:id>', methods=['GET'])
def product_detail(id):
    if request.method == 'GET':
        product = Product.query.get(id)
        if product:
            return jsonify({'product': product.serialize()})
        else:
            return jsonify({'message': 'Product not found.', 'status': 'failed'})
    return jsonify({'message': 'Invalid request.', 'status': 'failed'})

@app.route('/add/<int:id>', methods=['POST'])
@jwt_required()
def add_to_cart(id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({'message': 'User not found.', 'status': 'failed'}), 404

    product = Product.query.get_or_404(id)
    if product:
        quantity = 1
        cart_item = Cart.query.filter_by(product_id=id, user_id=current_user.id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = Cart(
                user_id=current_user.id,
                product_id=product.id,
                quantity=quantity,
                category=product.category,
                image=product.image
            )
            db.session.add(cart_item)
        db.session.commit()
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        return jsonify({'message': 'Product added to cart successfully!', 'cart_items': [item.serialize() for item in cart_items], 'subtotal': subtotal, 'status': 'success'})
    else:
        return jsonify({'message': 'Product not found.', 'status': 'failed'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)

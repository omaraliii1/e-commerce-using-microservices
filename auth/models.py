from flask_login import UserMixin
from extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

    def get_id(self):
        return str(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'address': self.address
        }


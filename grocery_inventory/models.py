from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid

from werkzeug.security import generate_password_hash, check_password_hash

import secrets

from flask_login import LoginManager, UserMixin

from flask_marshmallow import Marshmallow

db = SQLAlchemy()

login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Creating User Table
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True, default = '')
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    item = db.relationship('Item', backref = 'owner', lazy = True)

    def __init__(self, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)


    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)

# Creating Item table
class Item(db.Model):
    productId = db.Column(db.String, primary_key= True)
    brand = db.Column(db.String(50))
    category = db.Column(db.String(25))
    size = db.Column(db.String)
    description = db.Column(db.String(50))
    aisleLocation = db.Column(db.Integer)
    price = db.Column(db.Numeric(precision = 5, scale = 2))
    countryOrigin = db.Column(db.String)
    temperature = db.Column(db.Numeric(precision = 3, scale = 1))
    upc = db.Column(db.String, nullable = False)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, brand, category, size, description, aisleLocation, price, countryOrigin, temperature, upc, user_token, productId = ''):
        self.productId = self.set_id()
        self.brand = brand
        self.category = category
        self.size = size
        self.description = description
        self.aisleLocation = aisleLocation
        self.price = price
        self.countryOrigin = countryOrigin
        self.temperature = temperature
        self.upc = upc
        self.user_token = user_token

    def set_id(self):
        return (secrets.token_urlsafe())


# Creating marshaller
class ItemSchema(ma.Schema):
    class Meta:
        fields = ['productId', 'brand', 'category', 'size', 'description', 'aisleLocation', 'price', 'countryOrigin', 'temperature', 'upc', 'user_token']

item_schema = ItemSchema()
items_schema = ItemSchema(many = True)


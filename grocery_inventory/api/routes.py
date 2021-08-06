from flask import Blueprint, json, jsonify, request
from flask_migrate import current
from werkzeug.wrappers import response
from grocery_inventory.helpers import token_required
from grocery_inventory.models import db, User, Item, item_schema, items_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 800}


# route to create item
@api.route('/items', methods = ['POST'])
@token_required
def create_item(current_user_token):
    brand = request.json['brand']
    category = request.json['category']
    size = request.json['size']
    description = request.json['description']
    aisleLocation = request.json['aisleLocation']
    price = request.json['price']
    countryOrigin = request.json['countryOrigin']
    temperature = request.json['temperature']
    upc = request.json['upc']
    user_token = current_user_token.token

    item = Item(brand, category, size, description, aisleLocation, price, countryOrigin, temperature, upc, user_token = user_token)

    db.session.add(item)
    db.session.commit()

    response = item_schema.dump(item)
    return jsonify(response)

# route to retrieve multiple items
@api.route('/items', methods = ['GET'])
@token_required
def get_items(current_user_token):
    owner = current_user_token.token
    items = Item.query.filter_by(user_token = owner).all()
    response = items_schema.dump(items)
    return jsonify(response)

# route to retrieve one item
@api.route('/items/<id>', methods = ['GET'])
@token_required
def get_item(current_user_token, id):
    item = Item.query.get(id)
    response = item_schema.dump(item)
    return jsonify(response)
    
# route to update an item
@api.route('/items/<id>', methods = ['POST'])
@token_required
def update_item(current_user_token, id):
    item = Item.query.get(id)
    if item:
        item.brand = request.json['brand']
        item.category = request.json['category']
        item.size = request.json['size']
        item.description = request.json['description']
        item.aisleLocation = request.json['aisleLocation']
        item.price = request.json['price']
        item.countryOrigin = request.json['countryOrigin']
        item.temperature = request.json['temperature']
        item.upc = request.json['upc']
        item.user_token = current_user_token.token

        db.session.commit()

        response = item_schema.dump(item)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That item does not exist :('})

# Delete item endpoint
@api.route('/items/<id>', methods = ['DELETE'])
@token_required
def delete_item(current_user_token, id):
    item = Item.query.get(id)
    if item:
        db.session.delete(item)
        db.session.commit()

        response = item_schema.dump(item)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That item does not exist :('})

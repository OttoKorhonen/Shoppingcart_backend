from flask import Flask, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask.globals import request
import json
import os

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(os.environ['APP_SETTINGS'])
CORS(app)
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_COOKIE_SAMESITE'] = None


class Product(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    product_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    availability = db.Column(db.String, nullable=False)
    image_link = db.Column(db.String, nullable=True)
    condition = db.Column(db.String, nullable=False)
    brand = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f' { self.product_name} {self.description} {self.price} {self.availability} {self.image_link} {self.condition} {self.brand}'


@app.before_first_request
def initDb():

    if not db.session.query(Product).first():

        db.create_all()
        with open('dummy_data.json') as data:
            print('Initializing database')
            data = json.load(data)

        for prod in data:
            product = Product(**prod)

            db.session.add(product)

        db.session.commit()

        return jsonify(data)

    return jsonify({'status': 200, 'message': 'Database initialized'})


@app.route('/api/add', methods=['POST'])
def add_to_products():
    sent_item = request.get_json()
    allowed_fields = ['product_name', 'description', 'price', 'availability',
                      'image_link', 'condition', 'brand']

    product = Product()

    for key in sent_item:
        if key not in allowed_fields:
            raise ValueError
        if not hasattr(product, key):
            raise KeyError

        setattr(product, key, sent_item[key])

    db.session.add(product)
    db.session.commit()

    return jsonify({'status': 200})


@app.route('/api/edit/<int:id>', methods=['PUT'])
def edit_product(id=None):
    sent_item = request.get_json()
    product = Product.query.get(id)
    allowed_fields = ['product_name', 'description', 'price', 'availability',
                      'image_link', 'condition', 'brand']

    for key in sent_item:
        if key not in allowed_fields:
            raise ValueError
        if not hasattr(product, key):
            raise KeyError

        setattr(product, key, sent_item[key])

    db.session.add(product)
    db.session.commit()

    return jsonify({'status': 200, 'edited': id})


@app.route('/api/deleteproduct/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'status': 200, 'deleted': id})


@app.route('/api/getproduct/<int:id>', methods=['GET'])
def get_product(id):

    res = []
    product = Product.query.get(id)
    res.append({'id': product.id,
                'product_name': product.product_name,
                'price': product.price,
                'description': product.description,
                'availability': product.availability,
                'image_link': product.image_link,
                'condition': product.condition,
                'brand': product.brand})

    return jsonify(res)


@app.route('/api/allproducts', methods=['GET'])
def all_products():

    res = []
    for product in Product.query.all():
        res.append({
            'id': int(product.id),
            'product_name': product.product_name,
            'description': product.description,
            'price': product.price,
            'availability': product.availability,
            'image_link': product.image_link,
            'condition': product.condition,
            'brand': product.brand
        })

    return jsonify(res)


@app.route('/api/shoppingcart', methods=['GET'])
def shoppingcart():
    result = {
        'products': [],
        'total': 0,
        'status': 'Success'
    }
    current_cart = session.get('shoppingcart', {})

    res = create_products(result, current_cart)

    return jsonify(res)


def get_product(id: int):
    try:
        if Product.query.get(id):
            return Product.query.get(id)
    except:
        raise ValueError('Id not found')


def create_products(result, current_cart):

    total = 0

    for productId in current_cart:
        product = get_product(productId)

        p = {
            'id': int(product.id),
            'product_name': product.product_name,
            'availability': product.availability,
            'price': product.price,
            'description': product.description,
            'image_link': product.image_link,
            'brand': product.brand,
            'condition': product.condition,
            'count': current_cart[productId]
        }
        result['products'].append(p)

        total += product.price * p['count']

    result['total'] = total

    return result


@app.route("/api/shoppingcart", methods=['POST'])
def add_item_in_cart():

    result = {
        'products': [],
        'total': 0,
        'status': 'Success'
    }

    current_cart = session.get('shoppingcart', {})
    new_item = request.get_json()

    try:
        new_product = get_product(new_item['id'])
        count = int(new_item.get('count', 1))
        if count > 0:
            # sessio käyttää avaimina stringiä
            current_cart[str(new_product.id)] = count
            session['shoppingcart'] = current_cart

        else:
            raise ValueError

    except ValueError:
        result['status'] = 'Product not found.'
    except KeyError:
        result['status'] = f'Product by id {new_item["id"]} couldn`t be found.'

    res = create_products(result, current_cart)

    return jsonify(res)


@app.route('/api/shoppingcart/<int:id>', methods=['DELETE'])
def delete_from_cart(id):
    result = {
        'products': [],
        'total': 0,
        'status': 'Success'
    }
    current_cart = session.get('shoppingcart', {})

    total = 0
    if str(id) in current_cart:
        current_cart.pop(str(id))
        session['shoppingcart'] = current_cart = current_cart

        for productId in current_cart:
            product = get_product(productId)

            p = {
                'id': int(product.id),
                'product_name': product.product_name,
                'availability': product.availability,
                'price': product.price,
                'description': product.description,
                'image_link': product.image_link,
                'brand': product.brand,
                'condition': product.condition,
                'count': current_cart[productId]
            }
            result['products'].append(p)

            total += product.price * p['count']

    result['total'] = total

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)

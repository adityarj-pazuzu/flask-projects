from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import *

app = Flask(__name__)
app.secret_key = 'ggwp'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', required=True)

    @jwt_required()
    def get(self, name):
        item = [i for i in items if i['name'] == name]
        '''for i in items:
            if i['name'] == name:
                return i
        '''
        return {'item': item}, 200 if len(item) != 0 else 404

    def post(self, name):
        if len([i for i in items if i['name'] == name]) != 0:
            return {'message': f'Item with name "{name}" already exists'}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        for i in range(len(items)):
            if items[i].get('name') == name:
                del items[i]
                break

        return {'message': 'item deleted'}

    def put(self, name):
        data = Item.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)

        return item


class ItemList(Resource):
    def get(self):
        return {'item': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(debug=True)

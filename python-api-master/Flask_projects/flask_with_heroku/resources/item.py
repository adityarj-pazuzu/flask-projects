from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', required=True)
    parser.add_argument('store_id', required=True)

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {"message": "item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'Item with name "{name}" already exists'}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "Insertion failed"}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        #With Lambda
        #return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}
        return {"items": [i.json() for i in ItemModel.query.all()]}


from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from models.item import ItemModel
from schemas.item import ItemSchema

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item), 200

        return {"message": "Item not found"}, 404

    @jwt_required(fresh=True)
    def post(self, name: str):
        if ItemModel.find_by_name(name):
            return {"message": f"{name} already exists"}, 400

        item_json = request.get_json()
        item_json['name'] = name

        item = item_schema.load(item_json)

        try:
            item.save_to_db()
        except Exception as e:
            return {"message": f"Unable to add item <br>" f"{str(e)}</br>"}, 500

        return item_schema.dump(item), 201

    @jwt_required()
    def delete(self, name: str):
        try:
            ItemModel.find_by_name(name).delete_from_db()
            return {"message": "Item deleted from database"}, 200
        except Exception as e:
            return {"message": f"{str(e)}"}

    def put(self, name: str):
        item_json = request.get_json()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = item_json['price']
        else:
            item_json['name'] = name
            item = item_schema.load(item_json)

        item.save_to_db()

        return item.json(), 200


class ItemList(Resource):
    def get(self):
        return {"items": item_list_schema.dump(ItemModel.find_all())}, 200

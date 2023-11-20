from flask_restful import Resource

from schemas.store import StoreSchema
from models.store import StoreModel

store_schema = StoreSchema()
store_schema_list = StoreSchema(many=True)


class Store(Resource):
    def get(self, name: str):
        store = StoreModel.find_by_name(name)

        if store:
            return store_schema.dump(store), 200
        return {"message": "Store not found"}, 404

    def post(self, name: str):
        if StoreModel.find_by_name(name):
            return {"message": f"{name} Store already exists"}, 400

        store = StoreModel(name=name)

        try:
            store.save_to_db()
        except Exception as e:
            return {"message": f"Cannot Create store " f"*{str(e)}*"}, 500

        return store_schema.dump(store), 201

    def delete(self, name: str):
        try:
            StoreModel.find_by_name(name).delete_from_db()
            return {"message": "Store deleted"}, 201

        except Exception as e:
            return {"message": "Cannot delete the store \n" f"{str(e)}"}


class StoreList(Resource):
    def get(self):
        return {"message": store_schema_list.dump(StoreModel.find_all())}, 200

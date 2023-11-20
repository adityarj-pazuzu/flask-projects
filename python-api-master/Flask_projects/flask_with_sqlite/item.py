import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', required=True)

    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)

        if item:
            return item
        return {"message": "item not found"}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "select * from items where name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        connection.close()

        if row:
            return {"item": {"name": row[0], "price": row[1]}}

    def post(self, name):
        if Item.find_by_name(name):
            return {'message': f'Item with name "{name}" already exists'}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        try:
            Item.insert(item)
        except Exception as e:
            return {"message": f"Insertion failed\n{e.message}"}, 500

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "insert into items values (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "delete from items where name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = Item.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item:
            try:
                self.update(updated_item)
            except:
                return {"message": "Insert error in put"}
        else:
            try:
                self.insert(updated_item)
            except:
                return {"message": "Update error"}

        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "update items set price = ? where name = ?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "select * from items"
        result = cursor.execute(query)
        items = []

        for i in result:
            items.append({'name': i[0], 'price': i[1]})

        connection.close()

        return items

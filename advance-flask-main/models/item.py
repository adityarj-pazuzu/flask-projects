from typing import Dict, List

from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey("stores.store_id"))
    store = db.relationship("StoreModel", back_populates="items")

    def __init__(self, item_name: str, price: float, store_id: int):
        self.name = item_name
        self.price = price
        self.store_id = store_id

    def json(self) -> Dict:
        """Return Dictionary of Item data"""
        return {
            "item_id": self.item_id,
            "name": self.name,
            "price": self.price,
            "store_id": self.store_id,
        }

    @classmethod
    def find_by_name(cls, item_name: str):
        """Find row with item name"""
        return cls.query.filter_by(name=item_name).first()

    @classmethod
    def find_all(cls) -> List:
        """Return all rows from items table"""
        return cls.query.all()

    def save_to_db(self):
        """Save the data to database"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Delete the data from database"""

        db.session.delete(self)
        db.session.commit()

from typing import Dict, List

from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    store_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, name: str):
        self.name = name

    def json(self) -> Dict:
        """Return Dictionary of Store data"""
        return {
            "id": self.store_id,
            "name": self.name,
            "items": [item.json() for item in self.items.all()],
        }

    @classmethod
    def find_by_name(cls, name: str):
        """Find Store with name"""
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List:
        """Get all data from store table"""
        return cls.query.all()

    def save_to_db(self) -> None:
        """Save data to stores table"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """Delete data from stores table"""
        db.session.delete(self)
        db.session.commit()

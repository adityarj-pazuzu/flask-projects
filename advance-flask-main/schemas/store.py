from ma import ma
from models.store import StoreModel
from models.item import ItemModel
from schemas.item import ItemSchema

class StoreSchema(ma.SQLAlchemyAutoSchema):
    items = ma.Nested(ItemSchema, many=True)

    class Meta:
        model = StoreModel
        load_instance = True
        load_only = ("password",)
        dump_only = ("userid",)
        include_fk = True

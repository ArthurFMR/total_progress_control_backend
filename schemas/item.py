from marsh import marsh
from models.item import ItemModel
from models.list import ListModel

class ItemSchema(marsh.ModelSchema):
    class Meta:
        model = ItemModel
        load_only = ("list",)
        dump_only = ("item_id",)
        include_fk = True
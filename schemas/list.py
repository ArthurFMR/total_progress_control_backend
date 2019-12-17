from marsh import marsh
from models.list import ListModel
from models.user import UserModel
from schemas.item import ItemSchema

class ListSchema(marsh.ModelSchema):
    items = marsh.Nested(ItemSchema, many=True)

    class Meta:
        model = ListModel
        load_only = ("user",)
        load_only = ("items",)
        dump_only = ("list_id",)
        include_fk = True
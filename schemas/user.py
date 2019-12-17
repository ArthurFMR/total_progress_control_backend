from marsh import marsh
from models.user import UserModel
from models.list import ListModel
from schemas.list import ListSchema


class UserSchema(marsh.ModelSchema):
    lists = marsh.Nested(ListSchema, many=True)

    class Meta:
        model = UserModel
        load_only = ("password", "lists")
        dumb_only = ("user_id",)
        include_fk = True
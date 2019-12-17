import sqlite3

from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import(
    create_access_token,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from models.item import ItemModel
from schemas.item import ItemSchema
from models.list import ListModel


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


class Item(Resource):
    @classmethod
    def get(cls, _id: int):
        item = ItemModel.find_by_id(_id)

        if item:
            return item_schema.dump(item), 200
        return {"message": "item not found"}, 
    
    @classmethod
    def delete(cls, _id: int):
        item = ItemModel.find_by_id(_id)

        if item:
            item.delete_from_db()
            return {"message": "Item deleted"}, 200
        return {"message": "Item not found"}, 404

    @classmethod
    def put(cls, _id: int):
        item_json = request.get_json()
        item = ItemModel.find_by_id(_id)

        if item:
            item.title = item_json["title"]
            item.notes = item_json["notes"]
            item.total_qty = item_json["total_qty"]
            item.qty_done = item_json["qty_done"]

            try:
                item.save_to_db()
                return item_schema.dump(item), 200
            except:
                return {"message": "error saving to db, Update"}, 500
        return {"message": "Item not found"}, 404


class CreateItem(Resource):
    @classmethod
    def post(cls):
        item_json = request.get_json()
        if ListModel.find_by_id(item_json["list_id"]):
            if ItemModel.find_by_title_list_id(item_json["title"], item_json["list_id"]):
                return {"message": "A Item with this title already exists in your list"}, 400
            
            item = item_schema.load(item_json)

            try:
                item.save_to_db()
                return item_schema.dump(item)
            except:
                return {"message": "Item error inserting"}, 500
        return {"message": "The List type doesn't exists"}, 404
    

class Items(Resource):
    @classmethod
    def get(cls, list_id: int):
        return {"items": items_schema.dump(ItemModel.find_all(list_id))}, 200
        
    
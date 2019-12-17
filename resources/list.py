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
from models.list import ListModel
from schemas.list import ListSchema
from models.user import UserModel


list_schema = ListSchema()
lists_schema = ListSchema(many=True)


class List(Resource):
    @classmethod
    def get(cls, _id: int):
        _list = ListModel.find_by_id(_id)

        if _list:
            return list_schema.dump(_list), 200
        return {"message": "list not found"}, 
    
    @classmethod
    def delete(cls, _id: int):
        _list = ListModel.find_by_id(_id)

        if _list:
            _list.delete_from_db()
            return {"message": "List deleted"}, 200
        return {"message": "List not found"}, 404

    @classmethod
    def put(cls, _id: int):
        list_json = request.get_json()
        _list = ListModel.find_by_id(_id)

        if _list:
            _list.title = list_json["title"]

            try:
                _list.save_to_db()
                return list_schema.dump(_list), 200
            except:
                return {"message": "error saving to db, Update"}, 500
        return {"message": "list not found"}, 404


class CreateList(Resource):
    @classmethod
    def post(cls):
        list_json = request.get_json()
        if UserModel.find_by_id(list_json["user_id"]):

            if ListModel.find_by_title_user_id(list_json["title"], list_json["user_id"]):
                return {"message": "A list with this title already exists"}, 400
            
            _list = list_schema.load(list_json)
            
            try:
                
                _list.save_to_db()
                return list_schema.dump(_list), 200
            except:
                return {"message": "list error inserting"}, 500
        return {"message": "The user doesn't exists"}, 404
    

class Lists(Resource):
    @classmethod
    def get(cls, user_id: int):
        return {"lists": lists_schema.dump(ListModel.find_all(user_id))}, 200
        
    
    
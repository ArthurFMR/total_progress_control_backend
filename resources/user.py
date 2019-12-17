import sqlite3
import datetime

from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import(
    create_access_token,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from marshmallow import ValidationError
from models.user import UserModel
from schemas.user import UserSchema
from blacklist import BLACKLIST

user_schema = UserSchema()

class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)

        if UserModel.find_by_username(user.username):
            return {"message": "This Username already exist"}, 400

        user.save_to_db()
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=user.user_id, expires_delta=expires)
        return {"user": user_schema.dump(user), "access_token": access_token}, 201

class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json)

        user = UserModel.find_by_username(user_data.username)

        if user and safe_str_cmp(user.password, user_data.password):
            expires = datetime.timedelta(days=1)
            access_token = create_access_token(identity=user.user_id, expires_delta=expires)
            return {"user": user_schema.dump(user), "access_token": access_token}, 200
        
        return {"message": "Invalid credentials"}, 401

class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()['jti']
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        BLACKLIST.add(jti)
        return {"message": "{} Successfully log out".format(user.username)}
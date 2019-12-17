import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from marshmallow import ValidationError
from dotenv import load_dotenv

from sqlalch import db
from marsh import marsh
from blacklist import BLACKLIST

from resources.user import UserRegister, UserLogin, UserLogout
from resources.list import List, Lists, CreateList
from resources.item import Item, Items, CreateItem


app = Flask(__name__)
load_dotenv(".env")

app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

jwt = JWTManager(app)
@app.before_first_request
def create_tables():
    db.create_all()

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

api.add_resource(UserRegister, "/api/register")
api.add_resource(UserLogin, "/api/login")
api.add_resource(UserLogout, "/api/logout")
api.add_resource(CreateList, "/api/list/new")
api.add_resource(List, "/api/list/<int:_id>")
api.add_resource(Lists, "/api/lists/<int:user_id>")
api.add_resource(CreateItem, "/api/item/new")
api.add_resource(Item, "/api/item/<int:_id>")
api.add_resource(Items, "/api/items/<int:list_id>")


if __name__ == "__main__":
    db.init_app(app)
    marsh.init_app(app)
    app.run(debug=True)
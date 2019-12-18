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

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = "b'f1afa23342b5ef17079a34c76e1ae22a51dd475669b706f620489a481c35'"

api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

jwt = JWTManager(app)

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
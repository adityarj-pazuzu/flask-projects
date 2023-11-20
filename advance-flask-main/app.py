from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from marshmallow import ValidationError

from blacklist import blacklist
from db import db
from ma import ma
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import User, UserRegister, UserLogin, UserLogout, UserConfirm, TokenRefresh

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLE'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ["access", "refresh"]
app.secret_key = "asdf"

api = Api(app)


# Create database tables before first request
@app.before_first_request
def create_tables():
    db.create_all()

#Handle ValidationError throughout the app
@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify(e.messages), 400

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    """
    Function to check if access token is blacklisted. It will be called automatically if token is blacklisted
    This decorated function must take two arguments
    """

    return jwt_payload['jti'] in blacklist


api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")

api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:userid>")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(UserConfirm, "/user_confirm/<int:userid>")
api.add_resource(TokenRefresh, "/refresh")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(debug=True)

import json
import traceback

from flask import request, render_template, make_response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_restful import Resource

from blacklist import blacklist
from models.user import UserModel
from schemas.user import UserSchema

user_schema = UserSchema()


class UserRegister(Resource):
    def post(self):
        user = user_schema.load(request.get_json())

        if UserModel.find_by_username(user.username):
            return {"message": "user already exists"}, 400

        if UserModel.find_by_email(user.email):
            return {"message": "Email already exists"}, 400

        try:
            user.save_to_db()
            user.send_confirmation_email()
            return {"message": "User register successful. Check you email for activation link"}, 201
        except Exception as e:
            traceback.print_exc()
            return {"message": f"Error occurred while creating user <br> {str(e)}"}, 500


class User(Resource):
    @classmethod
    def get(cls, userid: int):
        user = UserModel.find_by_userid(userid)
        if not user:
            return {"message": "user not found"}, 404
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, userid: int):
        user = UserModel.find_by_userid(userid)
        if not user:
            return {"message": "user not found"}, 404
        user.delete_from_db()
        return {"message": "user deleted"}, 200


class UserLogin(Resource):
    def post(self):
        try:
            user_data = user_schema.load(request.get_json(), partial=("email",))

        except Exception as e:
            print(json.dumps(request.get_json()))
            return make_response((str(e)), 500)

        user = UserModel.find_by_username(user_data.username)

        if user and user.password == user_data.password:
            if user.activated:
                access_token = create_access_token(identity=user.userid, fresh=True)
                refresh_token = create_refresh_token(identity=user.userid)
                return {"access_token": access_token, "refresh_token": refresh_token}, 200
            return {"message": f"User {user.username} is not confirmed"}

        return {"message": "invalid credentials"}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        blacklist.add(jti)
        return {"message": "Logged out"}, 200


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        return {
                   "access_token": create_access_token(identity=current_user, fresh=False)
               }, 200


class UserConfirm(Resource):
    def get(self, userid: int):
        user = UserModel.find_by_userid(userid)
        if not user:
            return {"message": "User not found"}, 404

        user.activated = True
        user.save_to_db()
        header = {"Content-Type": "text/html"}
        # make_response can attach the response object to header
        return make_response(
                render_template('confirmation_page.html', email=user.email), 200, header
        )

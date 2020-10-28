from flask_restful import Resource, reqparse
from flask import request, json, jsonify, make_response, render_template
from flask_cors import CORS, cross_origin
from libs.mailer import MailerException
from models.user import *
from models.confirmation import ConfirmationModel
from schemas.user import UserSchema
import datetime as dt
import traceback

_5MIN = dt.timedelta(minutes=5)
schema = UserSchema()
login_schema = UserSchema(only=("email", "password"))
schema_many = UserSchema(many=True)

# class to login usersdt.datetime.now() +
class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = UserModel.get_data_()
        if not data:
            return {"message": "no data found"}, 404
        data = login_schema.load(data)
        msg, status = UserModel.login_checker(user_data=data)
        return msg, status


# class to register user
class UserRegister(Resource):
    @classmethod
    @jwt_optional
    def post(cls):
        claim = get_jwt_claims()
        data = schema.load(UserModel.get_data_())

        # check if data already exist
        unique_input_error, status = UserModel.post_unique_already_exist(claim, data)
        if unique_input_error:
            return unique_input_error, status

        # create user and send confirmation email
        msg, status_code = UserModel.create_user_send_confirmation(data=data)
        if status_code != 201:
            return msg, status_code
        return msg, status_code


# class to list all user
class UserList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        claim = get_jwt_claims()
        if not claim or not claim["is_admin"]:
            return {
                "message": ADMIN_PRIVILEDGE_REQUIRED.format("to get all users")
            }, 401

        users = UserModel.find_all()
        if users:
            return {"users": schema_many.dump(users)}, 201
        return {"message": NOT_FOUND.format("users")}, 400


# class to create user and get user
class User(Resource):
    @classmethod
    @jwt_required
    def get(cls, user_id=None):
        claim = get_jwt_claims()
        if not claim["is_admin"] and claim["userid"] != user_id:
            return {
                "message": ADMIN_PRIVILEDGE_REQUIRED.format("to get this users")
            }, 401

        user = UserModel.find_by_id(id=user_id)
        if user:
            return {"user": schema.dump(user)}, 201
        return {"message": NOT_FOUND.format("user")}, 400

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def put(cls, user_id):
        claim = get_jwt_claims()
        data = schema.load(UserModel.get_data_())

        # confirm the unique key to be same with the product route
        user, unique_input_error, status = UserModel.put_unique_already_exist(
            claim=claim, user_id=user_id, user_data=data
        )
        if unique_input_error:
            return unique_input_error, status
        if not claim["is_admin"]:
            data["admin"] = False

        # if user already exist update the dictionary
        if user:
            for each in data.keys():
                user.__setattr__(each, data[each])
            # save
            try:
                user.save_to_db()
                return schema.dump(user), 201
            except Exception as e:
                print(f"error is {e}")
                return {
                    "message": ERROR_WHILE_INSERTING.format("item")
                }, 500  # Internal server error
        return {"message": NOT_FOUND.format("user id")}, 400  # 400 is for bad request

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def delete(cls, user_id):
        claim = get_jwt_claims()
        user = UserModel.find_by_id(id=user_id)
        if claim and user:
            if not claim["is_root"] and user.rootusr:
                return {"message": CANNOT_DELETE_ROOT}, 401
            if not claim["is_admin"] and claim["user_id"] != user_id:
                return {
                    "message": ADMIN_PRIVILEDGE_REQUIRED.format("delete users")
                }, 401
        if user:
            user.delete_from_db()
            return {"message": DELETED.format("User")}, 200  # 200 ok
        return {"message": NOT_FOUND.format("User")}, 400  # 400 is for bad request


# to refresh token when it expires
class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        user_identity = get_jwt_identity()
        new_token = create_access_token(
            identity=user_identity, fresh=False, expires_delta=_5MIN
        )
        return {"access_token": new_token}, 200


# class to login users
class UserLogout(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        # second get  access
        # second get fresh
        jti1 = get_raw_jwt()["jti"]
        jti2 = decode_token(
            json.loads(request.get_data(as_text=True))["access_token"],
            allow_expired=True,
        )["jti"]
        BLACKLIST_ACCESS.add(jti1)
        BLACKLIST_ACCESS.add(jti2)
        return {"message": LODDED_OUT}, 200

from flask_restful import Resource, reqparse
from flask import request
from models.user import UserModel
from blacklist import BLACKLIST_REFRESH, BLACKLIST_ACCESS
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_optional,
    get_jwt_claims,
    get_jwt_identity,
    jwt_refresh_token_required,
    get_current_user,
    get_raw_jwt,
    get_csrf_token,
)
from error_messages import *
from schemas.user import UserSchema

reg_schema = UserSchema()
login_schema = UserSchema(only=("email", "password"))
reg_schema_many = UserSchema(many=True)

# class to login users
class UserLogin(Resource):
    @classmethod
    def post(cls):
        data_or_err,status = parser_or_err(login_schema,request.get_json())
        if status == 400: return data_or_err
        user = UserModel.find_by_email(data_or_err.get("email"))  # find user by email <2>

        if user and user.password == data_or_err.get("password"):  # check password <3>
            access_token = create_access_token(
                identity=user.id, fresh=True
            )  # create access token <4>
            refresh_token = create_refresh_token(
                identity=user.id
            )  # create refresh token <5>
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": INVALID_CREDENTIALS}, 401


# class to register user
class UserRegister(Resource):
    @classmethod
    @jwt_optional
    def post(cls):
        claim = get_jwt_claims()
        data_or_err,status = parser_or_err(reg_schema, request.get_json())
        if status == 400: return data_or_err

        # check if data already exist
        unique_input_error = UserModel.regpost_already_exist(data_or_err)
        if unique_input_error: return unique_input_error
        if not claim or not claim["is_admin"]: data_or_err["admin"] = False

        # insert
        try:
            user = UserModel(**data_or_err)
            user.save_to_db()
        except Exception as e:
            print(f"error is ----> {e}")
            return {
                "message": ERROR_WHILE_INSERTING.format("item")
            }, 500  # Internal server error

        return reg_schema.dump(user), 201


# class to list all user
class UserList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        claim = get_jwt_claims()
        if not claim or not claim["is_admin"]:
            return {"message": ADMIN_PRIVILEDGE_REQUIRED}, 401

        users = UserModel.find_all()
        if users:
            return {"users": reg_schema_many.dump(users)}, 201
        return {"message": NOT_FOUND.format("users")}, 400


# class to create user and get user
class User(Resource):
    @classmethod
    @jwt_required
    def get(cls, userid=None):
        claim = get_jwt_claims()
        if not claim["is_admin"] and claim["userid"] != userid:
            return {"message": ADMIN_PRIVILEDGE_REQUIRED}, 401

        user = UserModel.find_by_id(id=userid)

        if user:
            return {"user": reg_schema.dump(user)}, 201
        return {"message": "user not found"}, 400

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def put(cls, userid):
        claim = get_jwt_claims()
        if not claim["is_admin"] and claim["userid"] != userid:
            return {"message": ADMIN_PRIVILEDGE_REQUIRED}, 401

        data_or_err,status = parser_or_err(reg_schema, request.get_json())
        if status == 400: return data_or_err

        if not claim["is_admin"]: data_or_err["admin"] = False

        user = UserModel.find_by_id(id=userid)
        email = UserModel.find_by_email(email=data_or_err["email"])

        if user:
            # for product in products: product.update_cls_vars(data)
            if email and not (email.email == user.email):
                return {
                    "message": ALREADY_EXISTS.format("email", data_or_err["email"])
                }, 400  # 400 is for bad request
            # update
            try:
                for each in data_or_err.keys(): user.__setattr__(each, data_or_err[each])
                user.save_to_db()
            except Exception as e:
                print(f"error is {e}")
                return {
                    "message": ERROR_WHILE_INSERTING.format("item")
                }, 500  # Internal server error

        # confirm the unique key to be same with the product route
        else:
            user = UserModel(**data_or_err)
            if email:
                return {
                    "message": ALREADY_EXISTS.format("email", data_or_err["email"])
                }, 400  # 400 is for bad request
            try:
                user.save_to_db()
            except Exception as e:
                print(f"error is {e}")
                return {
                    "message": ERROR_WHILE_INSERTING.format("item")
                }, 500  # Internal server error

        return reg_schema.dump(user), 201

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def delete(cls, userid):
        claim = get_jwt_claims()
        if not claim["is_admin"] and claim["userid"] != userid:
            return {"message": ADMIN_PRIVILEDGE_REQUIRED}, 401

        user = UserModel.find_by_id(
            id=userid,
        )
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
        new_token = create_access_token(identity=user_identity, fresh=False)
        return {"access_token": new_token}, 200


# class to login users
class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        print(get_raw_jwt())
        jti = get_raw_jwt()["jti"]
        BLACKLIST_ACCESS.add(jti)
        return {"message": LODDED_OUT}, 200

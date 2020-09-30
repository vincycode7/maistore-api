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

schema = UserSchema()
login_schema = UserSchema(only=("email", "password"))
schema_many = UserSchema(many=True)

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
        data_or_err,status = parser_or_err(schema, request.get_json())
        if status == 400: 
            return data_or_err

        # check if data already exist
        unique_input_error, status = UserModel.post_unique_already_exist(claim, data_or_err)
        if unique_input_error: 
            return unique_input_error, status

        # insert
        user = UserModel(**data_or_err)
        try:
            user.save_to_db()
        except Exception as e:
            print(f"error is ----> {e}")
            return {"message": ERROR_WHILE_INSERTING.format("item")}, 500  # Internal server error
        return schema.dump(user), 201


# class to list all user
class UserList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        claim = get_jwt_claims()
        if not claim or not claim["is_admin"]:
            return {"message": ADMIN_PRIVILEDGE_REQUIRED.format("to get all users")}, 401

        users = UserModel.find_all()
        if users: 
            return {"users": schema_many.dump(users)}, 201
        return {"message": NOT_FOUND.format("users")}, 400


# class to create user and get user
class User(Resource):
    @classmethod
    @jwt_required
    def get(cls, userid=None):
        claim = get_jwt_claims()

        if not claim["is_admin"] and claim["userid"] != userid: 
            return {"message": ADMIN_PRIVILEDGE_REQUIRED.format("to get this users")}, 401

        user = UserModel.find_by_id(id=userid)
        if user: 
            return {"user": schema.dump(user)}, 201
        return {"message": "user not found"}, 400

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def put(cls, userid):
        claim = get_jwt_claims()
        data_or_err,status = parser_or_err(schema, request.get_json())

        # confirm the unique key to be same with the product route
        user,unique_input_error, status = UserModel.put_unique_already_exist(claim =claim, userid=userid, user_data=data_or_err)
        if unique_input_error: 
            return unique_input_error, status
        if status == 400: 
            return data_or_err
        if not claim["is_admin"]: 
            data_or_err["admin"] = False

        # if user already exist update the dictionary
        if user: 
            for each in data_or_err.keys(): user.__setattr__(each, data_or_err[each])
        else: 
            user = UserModel(**data_or_err)

        #save
        try: 
            user.save_to_db()
        except Exception as e:
            print(f"error is {e}")
            return {"message": ERROR_WHILE_INSERTING.format("item")}, 500  # Internal server error
        return schema.dump(user), 201

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def delete(cls, userid):
        claim = get_jwt_claims()
        if not claim["is_admin"] and claim["userid"] != userid: return {"message": ADMIN_PRIVILEDGE_REQUIRED.format("delete users")}, 401
        user = UserModel.find_by_id(id=userid)
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
        jti = get_raw_jwt()["jti"]
        BLACKLIST_ACCESS.add(jti)
        return {"message": LODDED_OUT}, 200
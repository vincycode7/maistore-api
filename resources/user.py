from flask_restful import Resource, reqparse
from models.user import UserModel
from blacklist import BLACKLIST_REFRESH, BLACKLIST_ACCESS
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_claims,
    get_jwt_identity,
    jwt_refresh_token_required,
    get_current_user,
    get_raw_jwt,
    get_csrf_token,
)
from error_messages import *

PARSER = reqparse.RequestParser()
PARSER.add_argument(
    name="firstname",
    type=str,
    required=False,
    help=TO_INPUT.format("firstname"),
    case_sensitive=False,
)
PARSER.add_argument(
    name="middlename",
    type=str,
    required=False,
    help=TO_INPUT.format("middlename"),
    case_sensitive=False,
)
PARSER.add_argument(
    name="lastname",
    type=str,
    required=False,
    help=TO_INPUT.format("lastname"),
    case_sensitive=False,
)
PARSER.add_argument(
    name="password", type=str, required=True, help=BLANK_ERROR.format("password")
)
PARSER.add_argument(
    name="email", type=str, required=True, help=BLANK_ERROR.format("email")
)
PARSER.add_argument(
    name="image", type=str, required=False, help=TO_INPUT.format("image")
)
PARSER.add_argument(
    name="phoneno", type=str, required=True, help=BLANK_ERROR.format("phoneno")
)
PARSER.add_argument(
    name="address",
    type=str,
    required=False,
    help=TO_INPUT.format("home address"),
    case_sensitive=False,
)
PARSER.add_argument(
    name="admin",
    type=bool,
    default=False,
    required=False,
    help=TO_INPUT.format("admin status (1 -- true, 0 -- false)"),
)
PARSER.add_argument(
    name="country",
    type=str,
    default=False,
    required=True,
    help=BLANK_ERROR.format("country"),
    case_sensitive=False,
)
PARSER.add_argument(
    name="lga",
    type=str,
    default=False,
    required=True,
    help=TO_INPUT.format("user's lga"),
    case_sensitive=False,
)
PARSER.add_argument(
    name="state",
    type=str,
    default=False,
    required=True,
    help=TO_INPUT.format("user's state"),
    case_sensitive=False,
)
# class to login users
class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        name="password", type=str, required=True, help=BLANK_ERROR.format("password")
    )
    parser.add_argument(
        name="email", type=str, required=True, help=BLANK_ERROR.format("email")
    )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()  # get data <1>
        user = UserModel.find_by_email(data.get("email"))  # find user by email <2>

        if user and user.password == data.get("password"):  # check password <3>
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
    def post(cls):
        data = PARSER.parse_args()

        # check if data already exist
        if UserModel.find_by_email(email=data["email"]):
            return {
                "message": ALREADY_EXISTS.format("email", data["email"])
            }, 400  # 400 is for bad request

        user = UserModel(**data)

        # insert
        try:
            user.save_to_db()
        except Exception as e:
            print(f"error is ----> {e}")
            return {
                "message": ERROR_WHILE_INSERTING.format("item")
            }, 500  # Internal server error

        return user.json(), 201


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
            return {"users": [user.json() for user in users]}, 201
        return {"message": NOT_FOUND.format("item")}, 400


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
            return {"user": user.json()}, 201
        return {"message": "user not found"}, 400

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def put(cls, userid):
        claim = get_jwt_claims()
        if not claim["is_admin"] and claim["userid"] != userid:
            return {"message": ADMIN_PRIVILEDGE_REQUIRED}, 401

        data = PARSER.parse_args()
        user = UserModel.find_by_id(id=userid)
        email = UserModel.find_by_email(email=data["email"])

        if user:
            # for product in products: product.update_cls_vars(data)
            if email and not (email.email == user.email):
                return {
                    "message": ALREADY_EXISTS.format("email", data["email"])
                }, 400  # 400 is for bad request
            # update
            try:
                for each in data.keys():
                    user.__setattr__(each, data[each])
                user.save_to_db()
            except Exception as e:
                print(f"error is {e}")
                return {
                    "message": ERROR_WHILE_INSERTING.format("item")
                }, 500  # Internal server error

        # confirm the unique key to be same with the product route
        else:
            user = UserModel(**data)
            if email:
                return {
                    "message": ALREADY_EXISTS.format("email", data["email"])
                }, 400  # 400 is for bad request
            try:
                user.save_to_db()
            except Exception as e:
                print(f"error is {e}")
                return {
                    "message": ERROR_WHILE_INSERTING.format("item")
                }, 500  # Internal server error

        return user.json(), 201

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

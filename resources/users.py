from flask_restful import Resource, reqparse
from flask import request, json, jsonify, make_response, render_template
from flask_cors import CORS, cross_origin
from libs.mailer import MailerException
from models.users import *
from models.confirmation import ConfirmationModel
from schemas.users import UserSchema
import datetime as dt
import traceback

_5MIN = dt.timedelta(minutes=5)
schema = UserSchema()
usr_reg_schema = UserSchema(only=("email", "password", "phoneno"))
login_schema = UserSchema(only=("email", "password"))
user_put_schema = UserSchema(exclude=("email", "password", "avatar", "admin", "rootusr"))
# email_reset_post_schema = UserSchema(only=("email", "new_email", "confirm_new_email"), unknown=EXCLUDE)
# password_reset_post_schema = UserSchema(exclude=("password", "new_password", "confirm_new_phoneno"))
schema_many = UserSchema(many=True)

# class to login usersdt.datetime.now() +
class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = UserModel.get_data_()
        if not data:
            return {"message": gettext("user_not_found")}, 404
        data = login_schema.load(data)
        try:
            msg, status = UserModel.login_checker(user_data=data)
        except Exception as e:
            print(e)
            return {"message" : gettext("Internal_server_error")}
        return msg, status


# class to register user
class UserRegister(Resource):
    @classmethod
    @jwt_optional
    def post(cls):
        data = usr_reg_schema.load(UserModel.get_data_())

        # check if data already exist
        unique_input_error, status = UserModel.post_unique_already_exist(data)
        if unique_input_error:
            return unique_input_error, status

        # create user and send confirmation email
        try:
            msg, status_code = UserModel.create_user_send_confirmation_digit(data=data)
        except Exception as e:
            print(e)
            return {"message": gettext("Internal_server_error")}, 500
        if status_code != 201:
            return msg, status_code
        return msg, status_code


# class to list all user
class UserList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        msg, status_code, _ = UserModel.auth_by_admin_root(
            get_err="user_req_ad_priv_to_get_users"
        )
        if status_code != 200:
            return msg, status_code

        users = UserModel.find_all()
        if users:
            return {"users": schema_many.dump(users)}, 201
        return {"message": gettext("user_not_found")}, 400


# class to create user and get user
class User(Resource):
    @classmethod
    @jwt_required
    def get(cls, user_id=None):
        msg, status_code, _ = UserModel.auth_by_admin_root_or_user(
            user_id=user_id, get_err="user_req_ad_priv_to_get_user"
        )
        if status_code != 200:
            return msg, status_code

        user = UserModel.find_by_id(id=user_id)
        if user:
            return {"user": schema.dump(user)}, 201
        return {"message": gettext("user_not_found")}, 404

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def put(cls, user_id):
        data = user_put_schema.load(UserModel.get_data_())

        # confirm the unique key to be same with the product route
        user, unique_input_error, status = UserModel.put_unique_already_exist(
            user_id=user_id, user_data=data
        )
        if unique_input_error:
            return unique_input_error, status

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
                    "message": gettext("Internal_server_error")
                }, 500  # Internal server error
        return {"message": gettext("user_not_found")}, 404

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def delete(cls, user_id):
        msg, status_code, _ = UserModel.auth_by_admin_root_or_user(
            user_id=user_id, get_err="user_deleted"
        )

        if status_code != 200:
            return msg, status_code

        user = UserModel.find_by_id(id=user_id)
        password = UserModel.get_data_().get("password", None)
        if user:
            if user.password == password:
                user.delete_from_db()
                return {"message": gettext("user_deleted")}, 200  # 200 ok
            elif user.password != password:
                return {
                    "messgae": gettext("user_password_auth_req_to_delete_user")
                }, 401
        return {"message": gettext("user_not_found")}, 404


# to refresh token when it expires
class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        user_identity = get_jwt_identity()
        user = UserModel.find_user_by_id(user_identity)
        if user:
            if not user.confirmed:
                jti = get_raw_jwt()["jti"]
                BLACKLIST_ACCESS.add(jti)
                return {"message": gettext("token_revoked")}, 401
        elif not user:
            jti = get_raw_jwt()["jti"]
            BLACKLIST_ACCESS.add(jti)
            return {"message": gettext("invalid_revoked")}, 401

        new_token = create_access_token(
            identity=user_identity, fresh=False, expires_delta=_5MIN
        )
        return {"access_token": new_token}, 200


# to refresh token when it expires
class Change_User_Email(Resource):
    @classmethod
    @jwt_required
    def post(cls, user_id):

        old_email = UserModel.get_data_().get("old_email", None)
        new_email = UserModel.get_data_().get("new_email", None)
        password = UserModel.get_data_().get("password", None)

        msg, status_code = UserModel.change_user_email(
            user_id=user_id, old_email=old_email, new_email=new_email, password=password
        )
        return msg, status_code


# to refresh token when it expires
class Change_User_Password(Resource):
    @classmethod
    @jwt_required
    def post(cls, user_id):
        old_password = UserModel.get_data_().get("old_password", None)
        new_password = UserModel.get_data_().get("new_password", None)

        msg, status_code = UserModel.change_user_password(
            user_id=user_id, old_password=old_password, new_password=new_password
        )
        return msg, status_code


# to refresh token when it expires (in development)
class Change_User_Image(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls, user_id):
        user_identity = get_jwt_identity()
        user = UserModel.find_user_by_id(user_id)
        print(f"identity --> {user_identity}, {user.confirmed}")
        if not user.confirmed:
            jti = get_raw_jwt()["jti"]
            BLACKLIST_ACCESS.add(jti)
            return {"message": "token_revoked"}, 401
        new_token = create_access_token(
            identity=user_identity, fresh=False, expires_delta=_5MIN
        )
        return {"access_token": new_token}, 200


# to refresh token when it expires
class Change_User_Admin_Status(Resource):
    @classmethod
    @jwt_required
    def post(cls, user_id):
        is_admin = cls.get_data_().get("is_admin", None)

        msg, status_code = UserModel.change_user_admin_status(
            user_id=user_id, is_admin=is_admin
        )
        return msg, status_code


# to refresh token when it expires
class Change_User_Root_Status(Resource):
    @classmethod
    @jwt_required
    def post(cls, user_id):
        is_root = cls.get_data_().get("is_root", None)

        msg, status_code = UserModel.change_user_root_status(
            user_id=user_id, is_root=is_root
        )
        return msg, status_code


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
        return {"message": gettext("user_logged_out")}, 200

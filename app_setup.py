from flask import Flask, request, jsonify
from blacklist import BLACKLIST_ACCESS
from marshmallow import ValidationError
from flask_restful import Api
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager
from flask_uploads import configure_uploads, patch_request_class
from libs.mailer import MailerException
from sqlalchemy import exc
from dotenv import load_dotenv
from libs.strings import gettext
from libs.image_helper import IMAGE_SET
import os


def config_app(app):
    app.config.from_object("config")
    app.config.from_envvar("APPLICATION_SETTINGS")
    return app


def create_usr_from_root(app):
    from models.users import UserModel, gettext

    data_usr = {
        "admin": True,
        "rootusr": True,
        "password": os.environ.get("ROOT_USR_PWD"),
        "email": os.environ.get("ROOT_USR_EMAIL"),
        "phoneno": os.environ.get("ROOT_USR_PHONE"),
    }
    # creat root user
    # check if data already exist
    unique_input_error, _ = UserModel.post_unique_already_exist(data_usr)
    if unique_input_error:
        print(f"{gettext('err_creating_root_usr').format(unique_input_error)}")
        return

    try:
        root_usr, _ = UserModel.create_user(data=data_usr)
    except Exception as e:
        UserModel.rollback_error()
        return

    try:
        confirmation = root_usr.create_confirmation()
    except Exception as e:
        root_usr.delete_from_db()
        UserModel.rollback_error()
        return

    try:
        confirmation.force_to_confirm()
        confirmation.force_to_expire()
    except Exception as e:
        root_usr.delete_from_db()
        confirmation.delete_from_db()
        print(gettext("err_confirming_root_usr").format(e))
        UserModel.rollback_error()
        return


def create_api(app):
    return Api(app=app)


def link_jwt(app):
    return JWTManager(app)  # creates a new end point called */auth*


def link_route_path(api, route_path):
    for route, path in route_path:
        api.add_resource(route, *path)
    return api


# def app_err_handler(app):
#     @app.errorhandler(exc.SQLAlchemyError)
#     def sqlalchemy_err(e):
#         return e


def jwt_error_handler(jwt):
    """
    Note here is more secure claim must be added here,
    where only one user can be the super user.
    And Only that user can create the first admin.
    """

    @jwt.user_claims_loader
    def add_claims_to_jwt(identity=None):
        from models.users import UserModel

        usr = UserModel.find_by_id(id=identity)
        if usr:
            return {"userid": identity, "is_root": usr.rootusr, "is_admin": usr.admin}
        return {"userid": identity, "is_root": False, "is_admin": False}

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        return decrypted_token["jti"] in BLACKLIST_ACCESS

    @jwt.expired_token_loader
    def expire_token_callback():
        return (
            jsonify({"message": gettext("token_expired")}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({"message": gettext("invalid_token")}),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback():
        return (
            jsonify(
                {
                    "message": gettext("authorization_required"),
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback():
        return (
            jsonify({"message": gettext("fresh_token_required")}),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback():
        return (
            jsonify({"message": gettext("token_revoked")}),
            401,
        )


def mash_err_handler(app):
    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        return {"message": str(err)}, 400


def create_and_config_app(app, route_path):
    load_dotenv(".env", verbose=True)
    cors = CORS(app)
    app = config_app(app)
    api = create_api(app)
    patch_request_class(app, size=10 * 1024 * 1024)  # 10MB max size upload
    configure_uploads(app, IMAGE_SET)
    jwt = link_jwt(app)
    mash_err_handler(app=app)
    jwt_error_handler(jwt)
    link_route_path(api=api, route_path=route_path)
    return app, cors, jwt, api

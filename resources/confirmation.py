import traceback
from time import time

from flask_restful import Resource
from flask import make_response, render_template
from flask_jwt_extended import jwt_required, get_jwt_claims

from models.users import UserModel
from db import db
from schemas.confirmation import ConfirmationSchema
from models.confirmation import ConfirmationModel
from libs.mailer import MailerException

confirmation_schema = ConfirmationSchema()
confirimation_schema_many = ConfirmationSchema(many=True)


# use to request for an eight digit forgot password code
class RequestConfirmationDigit(Resource):
    @classmethod
    def post(cls):
        """ send confirmation email """
        email = ConfirmationModel.get_data_().get("email", None)

        if email == None:
            return {
                "message": gettext("email_parameter_not_found")
            }, 404  # 400 is for bad request

        msg, status_code = ConfirmationModel.request_confirmation_digit(
            email=email, email_change=False
        )
        return msg, status_code


# use to confirm user
class ConfirmUser(Resource):
    @classmethod
    def post(cls, email: str):
        eight_digit = ConfirmationModel.get_data_().get("eight_digit", None)

        if eight_digit == None:
            return {
                "message": gettext("eight_digit_parameter_not_found")
            }, 404  # 400 is for bad request

        msg, status_code = ConfirmationModel.auth_confirmation(
            email=email, eight_digit=eight_digit
        )
        return msg, status_code


# use to view confirmations
class ViewConfirmation(Resource):
    @classmethod
    @jwt_required
    def get(cls, email: str):
        """ Returns confirmations for a given user. Use for testing """
        msg, status_code, _ = ConfirmationModel.auth_by_admin_root(
            get_err="confirmation_req_ad_priv_to_view_user_conf"
        )
        if status_code != 200:
            return msg, status_code

        user = UserModel.find_by_email(email=email)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        return (
            {
                "current_time": int(time()),
                "confirmations": [
                    confirmation_schema.dump(each)
                    for each in user.confirmation.order_by(ConfirmationModel.expire_at)
                ],
            },
            200,
        )

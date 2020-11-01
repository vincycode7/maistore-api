import traceback
from time import time

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_claims

from models.user import ForgotPasswordModel
from db import db
from error_messages import *
from models.forgot_password import ForgotPasswordModel
from schemas.forgot_password import ForgotPasswordSchema
from models.forgot_password import *
from libs.mailer import MailerException

forgotpassword_schema = ForgotPasswordSchema()
forgotpassword_schema_many = ForgotPasswordSchema(many=True)


# use to request for an eight digit forgot password code
class RequestForgotPasswordDigit(Resource):
    @classmethod
    def post(cls):
        email = ForgotPasswordModel.get_data_().get("email", None)

        if email == None:
            return {"message": NOT_FOUND.format("email parameter")}, 400  # 400 is for bad request 

        msg, status_code = ForgotPasswordModel.request_forgot_password_digit(email=email)
        return msg, status_code

# use to get the forgot password id by providing the eight digit code
class GetForgotPasswordId(Resource):
    @classmethod
    def post(cls, email: str):
        eight_digit = ForgotPasswordModel.get_data_().get("eight_digit", None)

        if email == None:
            return {"message": NOT_FOUND.format("email parameter")}, 400  # 400 is for bad request 

        msg, status_code = ForgotPasswordModel.get_forgot_password(email=email, eight_digit=eight_digit)
        return msg, status_code

# use to view a user's forgot password request
class ViewForgotPasswordRequests(Resource):
    @classmethod
    @jwt_required
    def get(cls, email: str):
        """ Returns forgot password requests for a given user. Use for testing """
        msg, status_code, _ = ForgotPasswordModel.auth_by_admin_root(err_msg="to get user confirmations")
        if status_code != 200:
            return msg, status_code

        user = ForgotPasswordModel.find_user_by_email(user_email=email)
        if not user:
            return {"message": NOT_FOUND.format("user")}, 404

        return (
            {
                "current_time": int(time()),
                "forgotpasswords": [
                    forgotpassword_schema.dump(each)
                    for each in user.forgotpassword.order_by(ForgotPasswordModel.expire_at)
                ],
            },
            200,
        )

# use to reset the user's password by providing both 
# the forgotpassword id and new password
class ResetPassword(Resource):
    @classmethod
    def post(cls, forgotpassword_id: str):
        new_password = ForgotPasswordModel.get_data_().get("new_password", None)

        if new_password == None:
            return {"message": NOT_FOUND.format("new_password parameter")}, 400  # 400 is for bad request 

        msg, status_code = ForgotPasswordModel.reset_password(
                                                                forgotpassword_id=forgotpassword_id, 
                                                                new_password=new_password
                                                                )
        return msg, status_code
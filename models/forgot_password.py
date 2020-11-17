# import packages
from models.models_helper import *
from requests import Response
from flask import request, url_for, make_response, render_template
from libs.mailer import Sender
from uuid import uuid4
from random import randint
from time import time

FORGOT_PASSWORD_EXPIRATION_DELTA = 1800  # 30 MINUTES

# class to create user and get user
class ForgotPasswordModel(db.Model, ModelsHelper):
    __tablename__ = "forgotpassword"

    # columns
    id = db.Column(db.String(50), primary_key=True, unique=True)
    expire_at = db.Column(db.Integer, unique=False, nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey("users.id"), nullable=False)
    used = db.Column(db.Boolean, nullable=False, default=False)
    eight_digit = db.Column(db.String(8), nullable=False)

    # merge (for sqlalchemy to link tables)

    def __init__(self, user_id: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.id = uuid4().hex
        self.expire_at = int(time()) + FORGOT_PASSWORD_EXPIRATION_DELTA
        self.eight_digit = str(randint(00000000, 99999999))

    @property
    def expired(self, get_err="fpass_err_getting_expired") -> bool:
        try:
            return time() > self.expire_at
        except Exception as e:
            raise ForgotPasswordException(gettext(get_err).format(e))

    def force_to_unused(self, get_err="fpass_err_forceunused") -> None:
        try:
            if self.used:
                self.used = False
                self.save_to_db(get_err="fpass_err_saving_fpass")
        except Exception as e:
            raise ForgotPasswordException(gettext(get_err).format(e))

    def force_to_used(self, get_err="fpass_err_forceused") -> None:
        try:
            if not self.used:
                self.used = True
                self.save_to_db(get_err="fpass_err_saving_fpass")
        except Exception as e:
            raise ForgotPasswordException(gettext(get_err).format(e))

    def force_to_expire(self, get_err="fpass_err_forceexpire") -> None:
        try:
            if not self.expired:
                self.expire_at = int(time())
                self.save_to_db(get_err="fpass_err_saving_fpass")
        except Exception as e:
            raise ForgotPasswordException(gettext(get_err).format(e))

    @classmethod
    def most_recent_fp_by_user_id(cls, user_id, get_err="fpass_err_getting_user_by_id"):
        try:
            return (
                cls.query.filter_by(user_id=user_id)
                .order_by(db.desc(cls.expire_at))
                .first()
            )
        except Exception as e:
            raise ForgotPasswordException(gettext(get_err).format(e))

    @classmethod
    def request_forgot_password_digit(cls, email):
        user = cls.find_user_by_email(user_email=email)

        if not user:
            return {"message": gettext("user_not_found")}, 404

        try:
            reply, status_code = user.create_send_forgotpassword_digit_for_user(
                user=user
            )
        except Exception as e:
            print(f"yaya --> {e}")
            return {"message": gettext("Internal_server_error")}, 500

        if status_code != 200:
            return reply, status_code

        return {"message": gettext("fpass_code_sent").format(user.email)}, 200

    @classmethod
    def get_forgot_password(cls, email, eight_digit):
        user = cls.find_user_by_email(user_email=email)

        if not user:
            return {"message": gettext("user_not_found")}, 404

        forgotpassword = user.most_recent_forgotpassword

        if not forgotpassword:
            return {"message": gettext("fpass_req_not_found")}, 404

        if forgotpassword.eight_digit != eight_digit:
            return {"message": gettext("fpass_incorrect_8_digit")}, 400

        return {"forgotpassword_id": forgotpassword.id}, 200

    @classmethod
    def reset_password(cls, forgotpassword_id, new_password):
        if new_password == None:
            return {
                "message": gettext("new_password_parameter_not_found")
            }, 404  # 404 is for bad request

        forgotpassword = cls.find_by_id(id=forgotpassword_id)

        if not forgotpassword:
            return {"message": gettext("fpass_req_not_found")}, 404  # Not found

        elif forgotpassword.used:
            return {"message": gettext("fpass_used")}, 400  # bad request

        elif forgotpassword.expired:
            return {"message": gettext("fpass_expired")}, 400  # bad request

        try:
            reply, status_code = forgotpassword.users.change_user_password(
                user_id=forgotpassword.user_id,
                new_password=new_password,
                forgot_old_password=True,
            )
            if status_code != 201:
                return reply, status_code

        except Exception as e:
            print(f"jarvis --> {e}")
            return {"message": gettext("Internal_server_error")}, 500
        try:
            forgotpassword.force_to_used()
            forgotpassword.force_to_expire()
        except Exception as e:
            print(e)
            return {"message": gettext("Internal_server_error")}, 500
        return {"message": gettext("password_reset_success")}, 200

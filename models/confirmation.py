# import packages
from models.models_helper import *
from requests import Response
from flask import request, url_for, make_response, render_template
from libs.mailer import Sender
from uuid import uuid4
from time import time
# from random import randint

CONFIRMATION_EXPIRATION_DELTA = 1800  # 30 MINUTES

# class to create user and get user
class ConfirmationModel(db.Model, ModelsHelper):
    __tablename__ = "confirmation"

    # columns
    id = db.Column(db.String(50), primary_key=True, unique=True)
    expire_at = db.Column(db.Integer, unique=False, nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey("user.id"), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    eight_digit = db.Column(db.String(8), nullable=False)

    # merge (for sqlalchemy to link tables)

    def __init__(self, user_id: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.id = uuid4().hex
        self.expire_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA
        self.eight_digit = str(randint(00000000, 99999999))

    @property
    def expired(self) -> bool:
        return time() > self.expire_at

    def force_to_unconfirm(self) -> None:
        if self.confirmed:
            self.confirmed = False
            self.save_to_db()

    def force_to_confirm(self) -> None:
        if not self.confirmed:
            self.confirmed = True
            self.save_to_db()

    def force_to_expire(self) -> None:
        if not self.expired:
            self.expire_at = int(time())
            self.save_to_db()

    @classmethod
    def most_recent_confirmation_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(db.desc(cls.expire_at)).first()

    @classmethod
    def request_confirmation_digit(cls,email,email_change=False):
        user = cls.find_user_by_email(user_email=email)

        if not user:
            return {"message": NOT_FOUND.format("user email")}, 400

        try:
            reply, status_code = user.create_send_confirmation_digit_for_user(user=user, email_change=email_change)

        except Exception as e:
            print(f"error is {e}")
            return {"message" : ERROR_WHILE.format("creating or sending confirming digit")}, 500

        if status_code != 200:
            return reply, status_code

        return {"message" : SENT_TO.format("8-digit code", user.email)}, 200

    @classmethod
    def auth_confirmation(cls, email, eight_digit):
        user = cls.find_user_by_email(user_email=email)

        if not user:
            return {"message": NOT_FOUND.format("user email")}, 404

        confirmation = user.most_recent_confirmation

        if not confirmation:
            return {"message": NOT_FOUND.format("no confirmation request found for user")}, 404
        
        if confirmation.eight_digit != eight_digit:
            return {"message": INVALID.format("8-digit code")}, 400

        if confirmation.confirmed:
            return {
                "message": ALREADY_CONFIRMED.format(
                    "user confirmation request", confirmation.id
                )
            }, 400 # bad request

        if confirmation.expired:
            return {"message": EXPIRED.format("user confirmation request")}, 400 # bad request

        try:
            confirmation.force_to_confirm()
            confirmation.force_to_expire()
        except Exception as e:
            print(e)
            return {"message" : ERROR_WHILE.format("confirming user")}, 500
        return {"message" : CONFIRMATION_SUCCESSFUL.format("user")}, 200


# import packages
from models.models_helper import *
from requests import Response
from flask import request, url_for, make_response, render_template
from libs.mailer import Sender
from uuid import uuid4
from time import time

CONFIRMATION_EXPIRATION_DELTA = 1800  # 30 MINUTES

# class to create user and get user
class ConfirmationModel(db.Model, ModelsHelper):
    __tablename__ = "confirmation"

    # columns
    id = db.Column(db.String(50), primary_key=True, unique=True)
    expire_at = db.Column(db.Integer, unique=False, nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey("user.id"), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)

    # merge (for sqlalchemy to link tables)
    # user = db.relationship("UserModel")

    def __init__(self, user_id: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.id = uuid4().hex
        self.expire_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA

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

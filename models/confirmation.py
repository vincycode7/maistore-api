# import packages
from models.models_helper import *
from requests import Response
from flask import request, url_for, make_response, render_template
from libs.mailer import Sender
from uuid import uuid4
from time import time
from random import randint

CONFIRMATION_EXPIRATION_DELTA = 1800  # 30 MINUTES

# class to create user and get user
class ConfirmationModel(db.Model, ModelsHelper):
    __tablename__ = "confirmation"

    # columns
    id = db.Column(db.String(50), primary_key=True, unique=True)
    expire_at = db.Column(db.Integer, unique=False, nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey("users.id"), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    eight_digit = db.Column(db.String(8), nullable=True)

    # merge (for sqlalchemy to link tables)

    def __init__(self, user_id: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.id = uuid4().hex
        self.expire_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA
        self.eight_digit = str(randint(10000000, 99999999))

    @property
    def expired(self) -> bool:
        try:
            return time() > self.expire_at
        except:
            raise ConfirmationException(gettext("confirmation_err_get_expired"))

    def force_to_unconfirm(
        self, get_err="confirmation_err_forceunconfirm_failed_to_save"
    ) -> None:
        try:
            if self.confirmed:
                self.confirmed = False
                self.save_to_db()
        except Exception as e:
            raise ConfirmationException(gettext(get_err).format(e))
        except:
            raise ConfirmationException(gettext(get_err))

    def force_to_confirm(
        self, get_err="confirmation_err_forceconfirm_failed_to_save"
    ) -> None:
        try:
            if not self.confirmed:
                self.confirmed = True
                self.save_to_db()
        except Exception as e:
            raise ConfirmationException(gettext(get_err).format(e))
        except:
            raise ConfirmationException(gettext(get_err))

    def force_to_expire(
        self, get_err="confirmation_err_forceexpire_failed_to_save"
    ) -> None:
        try:
            if not self.expired:
                self.expire_at = int(time())
                self.save_to_db()
        except Exception as e:
            raise ConfirmationException(gettext(get_err).format(e))
        except:
            raise ConfirmationException(gettext(get_err))

    @classmethod
    def most_recent_confirmation_by_user_id(
        cls, user_id, get_err="confirmation_err_get_mst_rct_conf"
    ):
        try:
            return (
                cls.query.filter_by(user_id=user_id)
                .order_by(db.desc(cls.expire_at))
                .first()
            )
        except Exception as e:
            raise ConfirmationException(gettext(get_err).format(e))
        except:
            raise ConfirmationException(gettext(get_err))

    @classmethod
    def request_confirmation_digit(cls, email, email_change=False):
        user = cls.find_user_by_email(user_email=email)

        if not user:
            return {"message": gettext("user_not_found")}, 404

        try:
            reply, status_code = user.create_send_confirmation_digit_for_user(
                user=user, email_change=email_change
            )
        # TODO: rewrite the error side into the localization
        except Exception as e:
            print(f"error is {e}")
            return {"message": gettext("user_err_sending_confirmation_digit")}, 500

        if status_code != 200:
            return reply, status_code

        return {"message": gettext("confirmation_code_sent").format(user.email)}, 200

    @classmethod
    def auth_confirmation(cls, email, eight_digit):
        user = cls.find_user_by_email(user_email=email)

        if not user:
            return {"message": gettext("user_not_found")}, 404

        try:
            confirmation = user.most_recent_confirmation
        except Exception as e:
            print(e)
            return {"message": gettext("Internal_server_error")}, 500
        if not confirmation:
            return {"message": gettext("confirmation_non_found")}, 404

        if confirmation.eight_digit != eight_digit:
            return {"message": gettext("confirmation_invalid_8_digit")}, 400

        if confirmation.confirmed:
            return {
                "message": gettext("user_confirmed").format(confirmation.id)
            }, 400  # bad request

        if confirmation.expired:
            return {
                "message": gettext("confirmation_8_digit_expired").format(eight_digit)
            }, 400  # bad request

        try:
            confirmation.force_to_confirm()
        except Exception as e:
            print(e)
            return {"message": gettext("Internal_server_error")}, 500

        try:
            confirmation.force_to_expire()
        except Exception as e:
            print(e)
            return {"message": gettext("Internal_server_error")}, 500

        return {"message": gettext("user_success_confirm_confirmation")}, 200

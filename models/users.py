# import packages
from uuid import uuid4
from requests import Response

from flask import request, url_for, make_response, render_template

from models.models_helper import *
from libs.mailer import MailerException, Sender
from models.confirmation import ConfirmationModel
from models.forgot_password import ForgotPasswordModel

# helper functions
def create_id(context):
    return "USER-V1-" + uuid4().hex

def _images(context):
    return context.image

# class to create user and get user
class UserModel(db.Model, ModelsHelper):
    __tablename__ = "users"

    # columns
    id = db.Column(db.String(50), primary_key=True, unique=True, default=create_id)
    lga = db.Column(db.String(30), nullable=True)
    state = db.Column(db.String(30), nullable=True)
    address = db.Column(db.String(300), nullable=True)
    middlename = db.Column(db.String(30), index=False, unique=False, nullable=True)
    lastname = db.Column(db.String(30), index=False, unique=False, nullable=True)
    firstname = db.Column(db.String(30), index=False, unique=False, nullable=True)
    created = db.Column(
        db.DateTime, index=False, unique=False, nullable=False, default=dt.now
    )
    country = db.Column(db.String(30))
    admin = db.Column(
        db.Boolean, index=False, unique=False, nullable=False, default=False
    )
    rootusr = db.Column(
        db.Boolean, index=False, unique=False, nullable=False, default=False
    )
    password = db.Column(db.String(80), index=False, unique=False, nullable=False)
    email = db.Column(db.String(100), index=False, unique=True, nullable=False)
    phoneno = db.Column(db.String(15), index=False, unique=True, nullable=True)
    avatar = db.Column(db.String, nullable=True, default=None)
    
    # merge (for sqlalchemy to link tables)
    stores = db.relationship(
        "StoreModel", lazy="dynamic", backref="users", cascade="all, delete-orphan"
    )
    bitcoins = db.relationship(
        "BitcoinPayModel", lazy="dynamic", backref="users", cascade="all, delete-orphan"
    )
    cards = db.relationship(
        "CardpayModel", lazy="dynamic", backref="users", cascade="all, delete-orphan"
    )
    favstores = db.relationship(
        "FavStoreModel", lazy="dynamic", backref="users", cascade="all, delete-orphan"
    )
    carts = db.relationship(
        "CartSystemModel", lazy="dynamic", backref="users", cascade="all, delete-orphan"
    )

    confirmation = db.relationship(
        "ConfirmationModel",
        lazy="dynamic",
        backref="users",
        cascade="all, delete-orphan",
    )

    forgotpassword = db.relationship(
        "ForgotPasswordModel",
        lazy="dynamic",
        backref="users",
        cascade="all, delete-orphan",
    )

    @property
    def confirmed(self, get_err="user_confirmed_status_failed_to_check"):
        confirmation = self.most_recent_confirmation
        try:
            if confirmation:
                return confirmation.confirmed
        except:
            raise UserException(gettext(get_err))
        return False

    @property
    def most_recent_confirmation(self, get_err="user_err_get_mst_rct_conf"):
        try:
            return self.confirmation.order_by(
                db.desc(ConfirmationModel.expire_at)
            ).first()
        except Exception as e:
            raise UserException(gettext(get_err).format(e))
        except:
            raise UserException(gettext(get_err))

    @property
    def most_recent_forgotpassword(self, get_err="user_err_get_mst_rct_fpass"):
        try:
            return self.forgotpassword.order_by(
                db.desc(ForgotPasswordModel.expire_at)
            ).first()
        except Exception as e:
            raise UserException(gettext(get_err).format(e))
        except:
            raise UserException(gettext(get_err))

    def create_confirmation(self, get_err="user_err_failed_to_create_confirmation"):
        try:
            confirmation = ConfirmationModel(self.id)
        except Exception as e:
            raise UserException(gettext(get_err).format(e))
        except:
            raise UserException(gettext(get_err))

        confirmation.save_to_db(get_err="user_err_failed_to_save_confirmation")
        return confirmation

    def create_forgotpassword(self, get_err="user_err_failed_to_create_fpass"):
        try:
            forgotpassword = ForgotPasswordModel(self.id)
        except Exception as e:
            raise UserException(gettext(get_err).format(e))
        except:
            raise UserException(gettext(get_err))

        forgotpassword.save_to_db(get_err="user_err_failed_to_save_fpass")
        return forgotpassword

    def send_confirmation_digit_toemail(
        self, get_err="user_err_sending_confirmation_digit"
    ):
        confirmation = self.most_recent_confirmation
        if not confirmation:
            raise UserException(gettext("user_err_no_confirmation_for_user"))

        to = [self.email]
        subject = "Confirmation 8-Digit Code"
        eight_digit = confirmation.eight_digit
        try:
            html = render_template("confirm_user.html", eight_digit=eight_digit)
        except Exception as e:
            raise UserException(gettext("user_err_getting_conf_code_html").format(e))

        try:
            sender = Sender()
            return (
                sender.send_email(
                    to=to, subject=subject, html=html, text=None, from_=None
                ),
                200,
            )
        except Exception as e:
            try:
                raise UserException(gettext(get_err).format(e))
            except:
                raise UserException(gettext(get_err))

    def request_new_forgot_password(self):
        """
        use to request for the forgot password 8-digit
        """
        most_recent_fp = self.most_recent_forgotpassword()
        if most_recent_fp:
            if not most_recent_fp.expired:
                most_recent_fp.force_to_expire()
        forgotpassword = self.create_forgotpassword()

        return forgotpassword, 200

    def send_forgotpassword_digit_toemail(
        self, get_err="user_err_sending_forgot_password_digit"
    ):
        forgotpassword = self.most_recent_forgotpassword
        if not forgotpassword:
            raise UserException(gettext("user_err_no_forgotpassreq_for_user"))

        to = [self.email]
        subject = "Password Reset 8-Digit Code"
        eight_digit = forgotpassword.eight_digit

        try:
            html = render_template("reset_password.html", eight_digit=eight_digit)
        except Exception as e:
            raise UserException(gettext("user_err_getting_fpass_html").format(e))
        try:
            sender = Sender()
            return (
                sender.send_email(
                    to=to, subject=subject, html=html, text=None, from_=None
                ),
                200,
            )
        except Exception as e:
            raise UserException(gettext(get_err).format(e))
        except:
            raise UserException(gettext(get_err))

    @classmethod
    def create_user(cls, data, get_err="user_err_failed_to_create_user"):
        try:
            user = cls(**data)  # create user
        except Exception as e:
            raise UserException(gettext(get_err).format(e))
        except:
            raise UserException(gettext(get_err))

        user.save_to_db(get_err="user_err_failed_to_save")  # save user

        return user, 200

    @classmethod
    def create_send_forgotpassword_digit_for_user(cls, user):
        forgotpassword = user.most_recent_forgotpassword
        if forgotpassword:
            forgotpassword.force_to_expire()
        forgotpassword = user.create_forgotpassword()

        try:
            user.send_forgotpassword_digit_toemail()
        except Exception as e:
            forgotpassword = user.most_recent_forgotpassword
            forgotpassword.delete_from_db(
                get_err="user_err_saving_forgot_password_request"
            )
            raise e
        return forgotpassword, 200

    @classmethod
    def create_send_confirmation_digit_for_user(cls, user, email_change=False):
        confirmation = user.most_recent_confirmation
        if confirmation:
            if not email_change and confirmation.confirmed:
                return {
                    "message": gettext("user_confirmation_already_confirmed").format(
                        confirmation.id
                    )
                }, 400
            confirmation.force_to_expire()
        confirmation = user.create_confirmation()

        try:
            user.send_confirmation_digit_toemail()
        except Exception as e:
            confirmation = user.most_recent_confirmation
            confirmation.delete_from_db(get_err="confirmation_err_failed_delete")
            raise e
        return confirmation, 200

    @classmethod
    def create_send_confirmation_for_user(cls, user, email_change=False):
        confirmation = user.most_recent_confirmation
        if confirmation:
            if not email_change and confirmation.confirmed:
                return {
                    "message": gettext("user_confirmation_already_confirmed").format(
                        confirmation.id
                    )
                }, 400
            confirmation.force_to_expire()
        confirmation = user.create_confirmation()

        try:
            user.send_confirmation_toemail()
        except Exception as e:
            confirmation = user.most_recent_confirmation
            confirmation.delete_from_db(get_err="confirmation_err_failed_delete")
            raise e
        return confirmation, 200

    @classmethod
    def create_user_send_confirmation(cls, data):
        # save user
        user, _ = cls.create_user(data)

        # send confirmation
        try:
            reply, status_code = cls.create_send_confirmation_for_user(
                user=user, email_change=False
            )
        except Exception as e:
            user.delete_from_db(get_err="user_err_falied_delete")
            raise e

        if status_code != 200:
            return reply, status_code
        return {
            "message": gettext("user_success_register_link").format(user.email)
        }, 200

    @classmethod
    def create_user_send_confirmation_digit(cls, data):
        # save user
        user, _ = cls.create_user(data)

        # send confirmation
        try:
            reply, status_code = cls.create_send_confirmation_digit_for_user(
                user=user, email_change=False
            )
        except Exception as e:
            user.delete_from_db()
            raise e

        if status_code != 200:
            return reply, status_code
        return {
            "message": gettext("user_success_register_digit").format(user.email)
        }, 200

    @classmethod
    def find_by_email(cls, email: str = None, get_err="user_err_find_by_email"):
        try:
            result = cls.query.filter_by(email=email).first()
        except Exception as e:
            raise UserException(gettext(get_err).format(e))
        except:
            raise UserException(gettext(get_err))
        return result

    @classmethod
    def find_by_phoneno(cls, phoneno: str = None, get_err="user_err_find_by_phoneno"):
        try:
            result = cls.query.filter_by(phoneno=phoneno).first()
        except Exception as e:
            raise UserException(gettext(get_err).format(e))
        except:
            raise UserException(gettext(get_err))
        return result

    @classmethod
    def login_checker(cls, user_data):
        import datetime as dt

        _5MIN = dt.timedelta(minutes=5)

        user = UserModel.find_by_email(user_data.get("email"))  # find user by email <2>
        if user and user.password == user_data.get("password"):
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:  # check password <3>
                try:
                    access_token = create_access_token(
                        identity=user.id, fresh=True, expires_delta=_5MIN
                    )  # create access token <4>
                    refresh_token = create_refresh_token(
                        identity=user.id
                    )  # create refresh token <5>
                except Exception as e:
                    raise UserException(
                        gettext("user_err_creating_access_refresh_token").format(e)
                    )
                except:
                    raise UserException(
                        gettext("user_err_creating_access_refresh_token")
                    )
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }, 200
            else:
                return {
                    "message": gettext("user_email_not_confirmed").format(
                        "email", user.email
                    )
                }, 400
        return {"message": gettext("user_invalid_login_credential")}, 401

    @classmethod
    def post_unique_already_exist(cls, user_data):
        
        phoneno = user_data.get("phoneno")
        email = user_data.get("email")
        user_by_phoneno = cls.find_by_phoneno(phoneno=phoneno)
        user_by_email = cls.find_by_email(email=email)
        
        # check if email already exist for another user
        unique_input_error, status = cls.post_email_already_exist(
            user_by_email=user_by_email, email=email
        )

        if unique_input_error:
            return unique_input_error, status

        # check if phone number already exist for another user
        unique_input_error, status = cls.post_phoneno_already_exist(
            user_by_phoneno=user_by_phoneno, phoneno=phoneno
        )

        if unique_input_error:
            return unique_input_error, status
        return False, 200

    @classmethod
    def post_email_already_exist(cls, user_by_email,email):
        if user_by_email:
            return {
                "message": gettext("user_email_exist").format(email)
            }, 400  # 400 is for bad request
        return None, 200

    @classmethod
    def post_phoneno_already_exist(cls, user_by_phoneno,phoneno):
        if user_by_phoneno:
            return {
                "message": gettext("user_phoneno_exist").format(phoneno)
            }, 400  # 400 is for bad request
        return None, 200

    @classmethod
    def put_unique_already_exist(cls, user_id, user_data):
        msg, status_code, claim = cls.auth_by_admin_root_or_user(
            user_id=user_id, get_err="user_req_ad_priv_to_edit"
        )
        if status_code != 200:
            return msg, status_code

        user_by_id = cls.find_by_id(id=user_id)
        user_by_phoneno = cls.find_by_phoneno(phoneno=user_data.get("phoneno"))

        # check if phone number already exist for another user
        user, unique_input_error, status = cls.put_phoneno_already_exist(
            user_by_id=user_by_id, user_by_phoneno=user_by_phoneno
        )

        if unique_input_error:
            return user, unique_input_error, status

        return user, False, 200

    @classmethod
    def put_phoneno_already_exist(cls, user_by_id, user_by_phoneno):

        # check if email already exist for another user
        if (
            user_by_id
            and user_by_phoneno
            and user_by_id.phoneno != user_by_phoneno.phoneno
        ):
            return (
                None,
                {
                    "message": gettext("user_phoneno_exist").format(
                        user_by_phoneno.phoneno
                    )
                },
                400,
            )  # 400 is for bad request
        return user_by_id, False, 200

    @classmethod
    def put_email_already_exist(cls, user_by_id, user_by_email):

        # check if email already exist for another user
        if user_by_id and user_by_email and user_by_id.email != user_by_email.email:
            return (
                None,
                {"message": gettext("user_email_exist").format(user_data.get("email"))},
                400,  # 400 is for bad request
            )  # 400 is for bad request
        return user_by_id, False, 200

    @classmethod
    def send_confirmation_on_email_change(cls, user):

        # check if mail will be sent to new email
        try:
            reply, status_code = cls.create_send_confirmation_for_user(
                user=user, email_change=True
            )
        except Exception as e:
            raise e

        if status_code != 200:
            return reply, status_code
        return {
            "message": gettext("user_success_send_confirmation").format(user.email)
        }, 200

    @classmethod
    def send_confirmation_digit_on_email_change(cls, user):

        # check if mail will be sent to new email
        try:
            reply, status_code = cls.create_send_confirmation_digit_for_user(
                user=user, email_change=True
            )
        except Exception as e:
            raise e

        if status_code != 200:
            return reply, status_code
        return {
            "message": gettext("user_success_send_confirmation_digit").format(
                user.email
            )
        }, 200

    @classmethod
    def change_user_email(cls, user_id, old_email, new_email, password):

        if old_email == None:
            return {"message": gettext("old_email_parameter_not_found")}, 404

        if new_email == None:
            return {"message": gettext("new_email_parameter_not_found")}, 404

        if password == None:
            return {"message": gettext("password_parameter_not_found")}, 404

        msg, status_code, _ = UserModel.auth_by_admin_root_or_user(
            user_id=user_id, get_err="user_auth_req_to_change_email"
        )
        if status_code != 200:
            return msg, status_code

        # check if user is using the same email
        if old_email == new_email:
            return {"message": gettext("same_email_nothing_to_change")}, 200

        user_by_id = cls.find_by_id(id=user_id)
        user_by_email = cls.find_by_email(email=new_email)
        user, unique_input_error, status = cls.put_email_already_exist(
            user_by_id=user_by_id, user_by_email=user_by_email
        )

        if unique_input_error:
            return unique_input_error, status

        # if user already exist update the dictionary
        if user:
            if user.password != password:
                return {"message": gettext("user_incorrect_password")}, 401
            if user.email != old_email:
                return {"message": gettext("user_incorrect_email")}, 401

            user.__setattr__("email", new_email)
            # save
            try:
                user.save_to_db(get_err="user_err_failed_to_save")
                # send confirmation to new email
                message, status_code = user.send_confirmation_digit_on_email_change(
                    user
                )
                if status_code == 200:
                    jti = get_raw_jwt()["jti"]
                    BLACKLIST_ACCESS.add(jti)
                    return message, status_code
                user.__setattr__("email", old_email)
                user.save_to_db(get_err="user_err_failed_to_save")
                return message, status_code
            except Exception as e:
                raise e
        return {"message": gettext("user_not_found")}, 404

    @classmethod
    def change_user_admin_status(cls, user_id, is_admin):
        if is_admin == None:
            return {"message": gettext("is_admin_parameter_not_found")}, 404

        msg, status_code, _ = UserModel.auth_by_admin_root(
            get_err="user_auth_req_to_change_admin_status"
        )
        if status_code != 200:
            return msg, status_code

        user = cls.find_by_id(id=user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404

        # if user already exist update the dictionary
        if user:
            user.__setattr__("admin", is_admin)
            # save
            try:
                user.save_to_db(get_err="user_err_failed_to_save")
            except Exception as e:
                raise e
        return {"message": gettext("user_success_update_admin_status")}, 200  # 200 ok

    @classmethod
    def change_user_root_status(cls, user_id, is_root):
        if is_root == None:
            return {"message": gettext("is_root_parameter_not_found")}, 404

        msg, status_code, _ = UserModel.auth_by_root(
            get_err="user_auth_req_to_change_root_status"
        )
        if status_code != 200:
            return msg, status_code

        user = cls.find_by_id(id=user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404

        # if user already exist update the dictionary
        if user:
            user.__setattr__("rootusr", is_root)
            # save
            try:
                user.save_to_db(get_err="user_err_failed_to_save")
            except Exception as e:
                raise e
        return {"message": gettext("user_success_update_admin_status")}, 200  # 200 ok

    @classmethod
    def change_user_password(
        cls, user_id, new_password, old_password=None, forgot_old_password=False
    ):

        if new_password == None:
            return {"message": gettext("new_password_parameter_not_found")}, 404

        user = UserModel.find_by_id(id=user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404

        if not forgot_old_password:
            # check if current user has permission to change password
            msg, status_code, _ = UserModel.auth_by_admin_root_or_user(
                user_id=user_id, get_err="user_req_ad_priv_to_change_password"
            )

            if status_code != 200:
                return msg, status_code

            # if old password is not provided
            if old_password == None:
                return {"message": gettext("old_password_parameter_not_found")}, 404

            # if password in database does not match old password
            if user.password != old_password:
                return {"message": gettext("user_incorrect_password")}, 401

            # check if old and new password are the same
            if old_password == new_password:
                return {"message": gettext("same_password_nothing_to_change")}, 200
        user.__setattr__("password", new_password)
        # save
        try:
            user.save_to_db()
        except Exception as e:
            raise e
        return {"message": gettext("user_success_update_password")}, 200  # 200 ok

    def __repr__(self) -> str:
        return f"{self.email}"

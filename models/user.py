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


# class to create user and get user
class UserModel(db.Model, ModelsHelper):
    __tablename__ = "user"

    # columns
    id = db.Column(db.String(50), primary_key=True, unique=True, default=create_id)
    lga = db.Column(db.String(30), nullable=True)
    state = db.Column(db.String(30), nullable=True)
    address = db.Column(db.String(300), nullable=True)
    image = db.Column(db.String(300), nullable=True)
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

    # merge (for sqlalchemy to link tables)
    stores = db.relationship(
        "StoreModel", lazy="dynamic", backref="user", cascade="all, delete-orphan"
    )
    bitcoins = db.relationship(
        "BitcoinPayModel", lazy="dynamic", backref="user", cascade="all, delete-orphan"
    )
    cards = db.relationship(
        "CardpayModel", lazy="dynamic", backref="user", cascade="all, delete-orphan"
    )
    favstores = db.relationship(
        "FavStoreModel", lazy="dynamic", backref="user", cascade="all, delete-orphan"
    )
    carts = db.relationship(
        "CartSystemModel", lazy="dynamic", backref="user", cascade="all, delete-orphan"
    )

    confirmation = db.relationship(
        "ConfirmationModel", lazy="dynamic", backref="user", cascade="all, delete-orphan"
    )

    forgotpassword = db.relationship(
        "ForgotPasswordModel", lazy="dynamic", backref="user", cascade="all, delete-orphan"
    )

    @property
    def confirmed(self):
        confirmation = self.most_recent_confirmation
        if confirmation:
            return confirmation.confirmed
        return False

    @property
    def most_recent_confirmation(self):
        return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()

    @property
    def most_recent_forgotpassword(self):
        return self.forgotpassword.order_by(db.desc(ForgotPasswordModel.expire_at)).first()

    def create_confirmation(self):
        confirmation = ConfirmationModel(self.id)
        confirmation.save_to_db()
        return confirmation

    def create_forgotpassword(self):
        forgotpassword = ForgotPasswordModel(self.id)
        forgotpassword.save_to_db()
        return forgotpassword
    
    def send_confirmation_toemail(self) -> Response:
        print("one -1 ")
        link = request.url_root[:-1] + url_for(
            "confirmuser", confirmation_id=self.most_recent_confirmation.id
        )  # get e.g http://maistore.com + /user_confirmation/1
        print("two")
        # from_ = "MAISTORE"
        to = [self.email]
        subject = "Registration confirmation"
        html = render_template("activate_email.html", link=link)
        sender = Sender()
        return sender.send_email(to=to, subject=subject, html=html, text=None)

    def send_confirmation_digit_toemail(self):
        from_ = "MAISTORE"
        eight_digit = self.most_recent_confirmation.eight_digit
        to = [self.email]
        subject = "Confirmation 8-Digit Code"
        html = render_template("confirm_user.html", eight_digit=eight_digit)
        sender = Sender()
        return sender.send_email(to=to, subject=subject, html=html, text=None)

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

    def send_forgotpassword_digit_toemail(self):
        from_ = "MAISTORE"
        eight_digit = self.most_recent_forgotpassword.eight_digit
        to = [self.email]
        subject = "Password Reset 8-Digit Code"
        html = render_template("reset_password.html", eight_digit=eight_digit)
        sender = Sender()
        return sender.send_email(to=to, subject=subject, html=html, text=None)

    @classmethod
    def create_user(cls, data):
        user = cls(**data)  # create user
        user.save_to_db() # save user
        return user
    
    @classmethod
    def create_send_forgotpassword_digit_for_user(cls, user):
        try:
            forgotpassword = user.most_recent_forgotpassword
            if forgotpassword:
                forgotpassword.force_to_expire()
            forgotpassword = user.create_forgotpassword()
        except Exception as e:
            raise e

        try:
            user.send_forgotpassword_digit_toemail()
        except Exception as e:
            forgotpassword = user.most_recent_forgotpassword
            forgotpassword.delete_from_db()
            raise e
        return None, 200

    @classmethod
    def create_send_confirmation_digit_for_user(cls, user, email_change=False):
        try:
            confirmation = user.most_recent_confirmation
            print("yaya")
            if confirmation:
                if not email_change and confirmation.confirmed:
                    return {
                        "message": ALREADY_CONFIRMED.format(
                            "user confirmation id", confirmation.id
                        )
                    }, 400
                confirmation.force_to_expire()
            print("bibi")
            confirmation = user.create_confirmation()
            print("kuku")
        except Exception as e:
            raise e

        try:
            user.send_confirmation_digit_toemail()
        except Exception as e:
            confirmation = user.most_recent_confirmation
            confirmation.delete_from_db()
            print("bloblo")
            raise e
        return None, 200

    @classmethod
    def create_send_confirmation_for_user(cls, user, email_change=False):
        try:
            confirmation = user.most_recent_confirmation
            print("yaya")
            if confirmation:
                if not email_change and confirmation.confirmed:
                    return {
                        "message": ALREADY_CONFIRMED.format(
                            "user confirmation id", confirmation.id
                        )
                    }, 400
                confirmation.force_to_expire()
            print("bibi")
            confirmation = user.create_confirmation()
            print("kuku")
        except Exception as e:
            raise e

        try:
            user.send_confirmation_toemail()
        except Exception as e:
            confirmation = user.most_recent_confirmation
            confirmation.delete_from_db()
            print("bloblo")
            raise e
        return None, 200
        
    @classmethod
    def create_user_send_confirmation(cls, data):
        # save user
        try:
            user = cls.create_user(data)
        except:
            traceback.print_exc()
            return {
                "message": ERROR_WHILE_INSERTING.format("user")
            }, 500  # Internal server error

        # send confirmation
        try:
            reply, status_code = cls.create_send_confirmation_for_user(user=user, email_change=False)

        except Exception as e:
            user.delete_from_db()
            print(e)
            return {
                "message": ERROR_WHILE.format("sending confirmation")
            }, 500  # Internal server error
        if status_code != 200:
                return reply, status_code
        return {"message": SUCCESS_REGISTER_MESSAGE.format(user.email)}, 201

    @classmethod
    def create_user_send_confirmation_digit(cls, data):
        # save user
        try:
            user = cls.create_user(data)
        except:
            traceback.print_exc()
            return {
                "message": ERROR_WHILE_INSERTING.format("user")
            }, 500  # Internal server error

        # send confirmation
        try:
            reply, status_code = cls.create_send_confirmation_digit_for_user(user=user, email_change=False)

        except Exception as e:
            user.delete_from_db()
            print(e)
            return {
                "message": ERROR_WHILE.format("sending confirmation")
            }, 500  # Internal server error
        if status_code != 200:
                return reply, status_code
        return {"message": SUCCESS_REGISTER_MESSAGE.format(user.email)}, 201

    @classmethod
    def find_by_email(cls, email: str = None):
        result = cls.query.filter_by(email=email).first()
        return result

    @classmethod
    def find_by_phoneno(cls, phoneno: str = None):
        result = cls.query.filter_by(phoneno=phoneno).first()
        return result

    @classmethod
    def login_checker(cls, user_data):
        import datetime as dt

        _5MIN = dt.timedelta(minutes=5)

        user = UserModel.find_by_email(user_data.get("email"))  # find user by email <2>
        if user and user.password == user_data.get("password"):
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:  # check password <3>
                access_token = create_access_token(
                    identity=user.id, fresh=True, expires_delta=_5MIN
                )  # create access token <4>
                refresh_token = create_refresh_token(
                    identity=user.id
                )  # create refresh token <5>
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }, 200
            else:
                return {"message": NOT_CONFIRMED_ERROR.format("email", user.email)}, 400
        return {"message": INVALID_CREDENTIALS}, 400

    @classmethod
    def post_unique_already_exist(cls, user_data):
        phoneno = cls.find_by_phoneno(phoneno=user_data.get("phoneno"))
        email = cls.find_by_email(email=user_data.get("email"))
        if email:
            return {
                "message": ALREADY_EXISTS.format("email", user_data["email"])
            }, 400  # 400 is for bad request
        if phoneno:
            return {
                "message": ALREADY_EXISTS.format("phoneno", user_data["phoneno"])
            }, 400  # 400 is for bad request
        return False, 200

    @classmethod
    def put_unique_already_exist(cls, user_id, user_data):
        user = cls.find_by_id(id=user_id)
        phoneno = cls.find_by_phoneno(phoneno=user_data.get("phoneno"))

        # check if phone number already exist for another user
        if user and phoneno and user.phoneno != phoneno.phoneno:
            return (
                None,
                {"message": ALREADY_EXISTS.format("phoneno", user_data["phoneno"])},
                400,
            )  # 400 is for bad request
        return user, False, 200

    @classmethod
    def email_already_exist(cls, user_id, email):
        user_by_id = cls.find_by_id(id=user_id)
        user_by_email = cls.find_by_email(email=email)

        # check if phone number already exist for another user
        if user_by_id and user_by_email and user_by_id.email != user_by_email.email:
            return (
                None,
                {"message": ALREADY_EXISTS.format("phoneno", user_data["phoneno"])},
                400,
            )  # 400 is for bad request
        return user_by_id, False, 200

    @classmethod
    def send_confirmation_on_email_change(cls, user):

        #check if mail will be sent to new email
        try:
            reply, status_code = cls.create_send_confirmation_for_user(user=user,email_change=True)

        except Exception as e:
            print(f"error is {e}")
            return {
                "message": ERROR_WHILE.format("sending confirmation to new email")
            }, 500  # Internal server error

        if status_code != 200:
                return reply, status_code
        return {"message": EMAIL_CHANGE_SUCCESSFULLY.format(user.email)}, 201

    @classmethod
    def send_confirmation_digit_on_email_change(cls, user):

        #check if mail will be sent to new email
        try:
            reply, status_code = cls.create_send_confirmation_digit_for_user(user=user, email_change=True)
        except Exception as e:
            print(f"error is {e}")
            return {
                "message": ERROR_WHILE.format("sending confirmation to new email")
            }, 500  # Internal server error

        if status_code != 200:
                return reply, status_code
        return {"message": EMAIL_CHANGE_SUCCESSFULLY.format(user.email)}, 201

    @classmethod
    def change_user_email(cls, user_id, old_email, new_email, password):

        user, unique_input_error, status = UserModel.email_already_exist(user_id=user_id, email=new_email)

        if unique_input_error:
            return unique_input_error, status

        # if user already exist update the dictionary
        if user:
            if user.email != old_email:
                return {"message" : INVALID_CREDENTIALS_FOR.format("email")}, 400
            elif user.password != password:
                return {"message" : INVALID_CREDENTIALS_FOR.format("password")}, 400

            user.__setattr__("email", new_email)
            # save
            try:
                user.save_to_db()
                # send confirmation to new email
                message, status_code = user.send_confirmation_digit_on_email_change(user)
                if status_code == 201:
                    jti = get_raw_jwt()['jti']
                    BLACKLIST_ACCESS.add(jti)
                    return message, status_code
                user.__setattr__("email", old_email)
                user.save_to_db()
                return message, status_code
            except Exception as e:
                print(f"error is {e}")
                return {
                    "message": ERROR_WHILE_INSERTING.format("user")
                }, 500  # Internal server error
        return {"message": NOT_FOUND.format("user id")}, 400  # 400 is for bad request  

    @classmethod
    def change_user_admin_status(cls, user_id, is_admin):

        user = cls.find_by_id(id=user_id)
        if not user:
            return {"message": NOT_FOUND.format("user id")}, 400  # 400 is for bad request 

        # if user already exist update the dictionary
        if user:
            user.__setattr__("admin", is_admin)
            # save
            try:
                user.save_to_db()
            except Exception as e:
                print(f"error is {e}")
                return {
                    "message": ERROR_WHILE_INSERTING.format("admin status")
                }, 500  # Internal server error
        return {"message": SUCCESS_UPDATE.format("admin status")}, 200  # 200 ok

    @classmethod
    def change_user_root_status(cls, user_id, is_root):

        user = cls.find_by_id(id=user_id)
        if not user:
            return {"message": NOT_FOUND.format("user id")}, 400  # 400 is for bad request

        # if user already exist update the dictionary
        if user:
            user.__setattr__("rootusr", is_root)
            # save
            try:
                user.save_to_db()
            except Exception as e:
                print(f"error is {e}")
                return {
                    "message": ERROR_WHILE_INSERTING.format("root status")
                }, 500  # Internal server error
        return {"message": SUCCESS_UPDATE.format("root status")}, 200  # 200 ok

    @classmethod
    def change_user_password(cls, user_id, new_password, old_password=None, forgot_old_password=False):

        user = UserModel.find_by_id(id=user_id)
        if not user:
            return {"message": NOT_FOUND.format("user id")}, 400  # 400 is for bad request 

        # if user already exist update the dictionary
        if not forgot_old_password:
            if user.password != old_password:
                return {"message" : INVALID_CREDENTIALS_FOR.format("password")}, 401

        user.__setattr__("password", new_password)
        # save
        try:
            user.save_to_db()
        except Exception as e:
            print(f"error is {e}")
            return {
                "message": ERROR_WHILE_INSERTING.format("new password")
            }, 500  # Internal server error
        return {"message": SUCCESS_UPDATE.format("new password")}, 201  # 200 ok

    def __repr__(self) -> str:
        return f"{self.email}"

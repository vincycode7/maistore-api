# import packages
from models.models_helper import *
# class to create user and get user
class UserModel(db.Model, ModelsHelper):
    __tablename__ = "user"

    # columns
    id = db.Column(db.Integer, primary_key=True, unique=True)
    lga = db.Column(db.String(30), nullable=True)
    state = db.Column(db.String(30), nullable=True)
    address = db.Column(db.String(300), nullable=True)
    image = db.Column(db.String(300), nullable=True)
    middlename = db.Column(db.String(30), index=False, unique=False, nullable=True)
    lastname = db.Column(db.String(30), index=False, unique=False, nullable=True)
    firstname = db.Column(db.String(30), index=False, unique=False, nullable=False)
    created = db.Column(
        db.DateTime, index=False, unique=False, nullable=False, default=dt.now
    )
    country = db.Column(db.String(30), nullable=False)
    admin = db.Column(
        db.Boolean, index=False, unique=False, nullable=False, default=False
    )
    password = db.Column(db.String(80), index=False, unique=False, nullable=False)
    email = db.Column(db.String(100), index=False, unique=True, nullable=False)
    phoneno = db.Column(db.String(15), index=False, unique=True, nullable=False)
    activated = db.Column(db.Boolean, default=False)

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

    @classmethod
    def find_by_email(cls, email: str = None):
        result = cls.query.filter_by(email=email).first()
        return result

    @classmethod
    def find_by_phoneno(cls, phoneno: str = None):
        result = cls.query.filter_by(phoneno=phoneno).first()
        return result

    @classmethod
    def check_unique_inputs(cls, user_data):
        email = cls.find_by_email(email=user_data["email"])
        phoneno = cls.find_by_phoneno(phoneno=user_data["phoneno"])
        return email, phoneno
    @classmethod
    def login_checker(cls, user_data):
        import datetime as dt
        _5MIN = dt.timedelta(minutes=5)

        user = UserModel.find_by_email(user_data.get("email"))  # find user by email <2>
        if user and user.password == user_data.get("password"):
            if user.activated:  # check password <3>
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
                return {"message": NOT_CONFIRMED_ERROR.format("email",user.email)}, 400
        return {"message": INVALID_CREDENTIALS}, 401

    @classmethod
    def post_unique_already_exist(cls, claim, user_data):
        email, phoneno = cls.check_unique_inputs(user_data=user_data)
        if email:
            return {
                "message": ALREADY_EXISTS.format("email", user_data["email"])
            }, 400  # 400 is for bad request
        elif phoneno:
            return {
                "message": ALREADY_EXISTS.format("phoneno", user_data["phoneno"])
            }, 400  # 400 is for bad request
        elif (not claim and user_data["admin"] == True) or (
            claim and not claim["is_admin"] and user_data["admin"] == True
        ):
            return {
                "message": ADMIN_PRIVILEDGE_REQUIRED.format("set admin status to true")
            }, 401
        return False, 200

    @classmethod
    def put_unique_already_exist(cls, claim, userid, user_data):
        user = cls.find_by_id(id=userid)
        email, phoneno = cls.check_unique_inputs(user_data=user_data)

        # check user permission, edit and parse data
        if not claim["is_admin"] and claim["userid"] != userid:
            return (
                user,
                {"message": ADMIN_PRIVILEDGE_REQUIRED.format("edit user data")},
                401,
            )
        elif not claim["is_admin"] and user_data["admin"] != True:
            return (
                user,
                {"message": ADMIN_PRIVILEDGE_REQUIRED.format("to change admin status")},
                401,
            )
        elif user and email and user.email != email.email:
            return (
                user,
                {"message": ALREADY_EXISTS.format("email", user_data["email"])},
                400,
            )  # 400 is for bad request
        elif user and phoneno and user.phoneno != phoneno.phoneno:
            return (
                user,
                {"message": ALREADY_EXISTS.format("phoneno", user_data["phoneno"])},
                400,
            )  # 400 is for bad request
        return user, False, 200

    def __repr__(self) -> str:
        return f"{self.email}"

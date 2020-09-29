# import packages
from db import db
from datetime import datetime as dt
from models.models_helper import ModelsHelper
from typing import List, Dict
from error_messages import *

# class to create user and get user
class UserModel(db.Model, ModelsHelper):

    __tablename__ = "user"

    # columns
    id = db.Column(db.Integer, primary_key=True, unique=True)
    lga = db.Column(db.String(30), nullable=True)
    state = db.Column(db.String(30), nullable=True)
    address = db.Column(db.String(300), nullable=True)
    image = db.Column(db.String(300), nullable=True)
    firstname = db.Column(db.String(30), index=False, unique=False, nullable=True)
    middlename = db.Column(db.String(30), index=False, unique=False, nullable=True)
    lastname = db.Column(db.String(30), index=False, unique=False, nullable=True)
    created = db.Column(db.DateTime, index=False, unique=False, nullable=False, default=dt.now)
    country = db.Column(db.String(30), nullable=False)
    admin = db.Column(db.Boolean, index=False, unique=False, nullable=False, default=False)
    password = db.Column(db.String(80), index=False, unique=False, nullable=False)
    email = db.Column(db.String(100), index=False, unique=True, nullable=False)
    phoneno = db.Column(db.String(15), index=False, unique=True, nullable=False)

    # merge (for sqlalchemy to link tables)
    stores = db.relationship("StoreModel", lazy="dynamic", cascade="all, delete-orphan")
    bitcoins = db.relationship("BitcoinPayModel", lazy="dynamic", cascade="all, delete-orphan")
    cards = db.relationship("CardpayModel", lazy="dynamic", cascade="all, delete-orphan")
    favstores = db.relationship("FavStoreModel", lazy="dynamic", cascade="all, delete-orphan")
    carts = db.relationship("CartSystemModel", lazy="dynamic", cascade="all, delete-orphan")

    # # a json representation
    # def json(self) -> Dict:
    #     return {
    #         "id": self.id,
    #         "profile": {
    #             "firstname": self.firstname,
    #             "lastname": self.lastname,
    #             "middlename": self.middlename,
    #             "phoneno": self.phoneno,
    #             "address": self.address,
    #             "image": self.image,
    #             "password": self.password,
    #             "email": self.email,
    #             "lga": self.lga,
    #             "state": self.state,
    #             "country": self.country,
    #         },
    #         "mystores": [store.json() for store in self.stores.all()],
    #         "paymentmethods": {
    #             "bitcoins": [coin.json() for coin in self.bitcoins.all()],
    #             "cards": [card.json() for card in self.cards.all()],
    #         },
    #         "favstores": [fav.json()["storeid"] for fav in self.favstores.all()],
    #         "mycarts": [cart.json() for cart in self.carts.all()],
    #     }

    @classmethod
    def find_all(cls) -> List:
        results = cls.query.all()  # the comma is required because it expects a tuple
        return results

    @classmethod
    def find_by_email(cls, email: str = None):
        result = cls.query.filter_by(email=email).first()
        return result
    
    @classmethod
    def find_by_phoneno(cls, phoneno: str = None):
        result = cls.query.filter_by(phoneno=phoneno).first()
        return result

    @classmethod
    def find_by_id(cls, id: int):
        result = cls.query.filter_by(id=id).first()
        return result

    @classmethod
    def regpost_already_exist(cls, user_data):
        if UserModel.find_by_email(email=user_data["email"]):
            return {
                "message": ALREADY_EXISTS.format("email", user_data["email"])
            }, 400  # 400 is for bad request
        elif UserModel.find_by_phoneno(phoneno=user_data["phoneno"]):
            return {
                "message": ALREADY_EXISTS.format("phoneno", user_data["phoneno"])
            }, 400  # 400 is for bad request
        return False

    def __repr__(self) -> str:
        return f"{self.email}"

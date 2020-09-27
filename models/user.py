#import packages
from db import db
from datetime import datetime as dt
from models.models_helper import ModelsHelper

#class to create user and get user
class UserModel(db.Model, ModelsHelper):

    __tablename__ = "user"

    # columns
    id = db.Column(db.Integer, primary_key=True, unique=True)
    lga = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(30), nullable=False)
    firstname = db.Column(db.String(30), index=False, unique=False, nullable=False)
    middlename = db.Column(db.String(30), index=False, unique=False, nullable=False)
    lastname = db.Column(db.String(30), index=False, unique=False, nullable=False)
    password = db.Column(db.String(80), index=False, unique=False, nullable=False)
    email = db.Column(db.String(100), index=False, unique=False, nullable=False)
    phoneno = db.Column(db.String(15), index=False, unique=False, nullable=False)
    created = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    address = db.Column(db.String(300))
    image = db.Column(db.String(300))
    admin = db.Column(db.Boolean, index=False, unique=False, nullable=False)

    #merge (for sqlalchemy to link tables)
    stores = db.relationship("StoreModel", lazy="dynamic")
    bitcoins = db.relationship("BitcoinPayModel", lazy="dynamic")
    cards = db.relationship("CardpayModel",lazy="dynamic")
    favstores = db.relationship("FavStoreModel", lazy="dynamic")
    carts = db.relationship("CartSystemModel", lazy="dynamic")

    # set children
    _childrelations = ['stores', 'bitcoins', 'cards', 'favstores', 'carts']

    def __init__(
                    self, password, phoneno, email, 
                    admin=False, country=None, state=None, 
                    lga=None, created=None, lastname=None, 
                    middlename=None, firstname=None, address=None,
                    image=None
                ):

        # Required 
        self.password = password
        self.phoneno = phoneno
        self.email = email

        #optional
        self.firstname = firstname
        self.lastname = lastname
        self.middlename = middlename
        self.address = address
        self.image = image
        self.admin = admin
        self.country = country
        self.state = state
        self.lga = lga
        self.created = created if created else dt.now()

    # a json representation
    def json(self):
        return {
                "id" : self.id,

                "profile"      : {   
                                    "firstname" : self.firstname,
                                    "lastname" : self.lastname,
                                    "middlename" : self.middlename,
                                    "phoneno" : self.phoneno,
                                    "address" : self.address,
                                    "image" : self.image,
                                    "password" : self.password,
                                    "email" : self.email,
                                    "lga" : self.lga,
                                    "state": self.state,
                                    "country" : self.country
                                    },

                "mystores"       : [store.json() for store in self.stores.all()],

                "paymentmethods" : {
                                    "bitcoins" : [coin.json() for coin in self.bitcoins.all()],
                                    "cards"    : [card.json() for card in self.cards.all()]
                                    },

                "favstores" : [fav.json()["storeid"] for fav in self.favstores.all()],
                "mycarts" : [cart.json() for cart in self.carts.all()],
                }

    @classmethod
    def find_all(cls):
        results = cls.query.all()  #the comma is required because it expects a tuple
        return results 

    @classmethod
    def find_by_email(cls, email=None):
        result = cls.query.filter_by(email=email).first()
        return result 

    @classmethod
    def find_by_id(cls, id):
        result = cls.query.filter_by(id=id).first()
        return result 

    def __repr__(self):
        return f"{self.email}"
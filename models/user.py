#import packages
from db import db
from datetime import datetime as dt

#class to create user and get user
class UserModel(db.Model):

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
    profilepic = db.Column(db.String(300))
    admin = db.Column(db.Boolean, index=False, unique=False, nullable=False)

    #merge (for sqlalchemy to link tables)
    stores = db.relationship("StoreModel", lazy="dynamic")
    bitcoins = db.relationship("BitcoinPayModel", lazy="dynamic")
    cards = db.relationship("CardpayModel",lazy="dynamic")
    favstores = db.relationship("FavStoreModel", lazy="dynamic")
    carts = db.relationship("CartSystemModel", lazy="dynamic")
    # purchased = db.relationship("PurchasedModel", lazy="dynamic") # one to many relationship
    # notifications = db.relationship("NoticeModel", lazy="dynamic")

    def __init__(
                    self, firstname, password, phoneno, 
                    email, admin, country, state, 
                    lga, created=None, lastname=None, 
                    middlename=None, address=None,
                    profilepic=None
                ):

        self.firstname = firstname
        self.lastname = lastname
        self.middlename = middlename
        self.password = password
        self.phoneno = phoneno
        self.email = email
        self.address = address
        self.profilepic = profilepic
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
                                    "profilepic" : self.profilepic,
                                    "password" : self.password,
                                    "email" : self.email,
                                    "lga" : self.lga,
                                    "state": self.state,
                                    "country" : self.country
                                    },

                "mystores"       : [store.json() for store in self.stores.all()],

                "paymentmethods" : {
                                    "bitcoins" : [coins.json() for coins in self.bitcoins.all()],
                                    "cards"    : [card.json() for card in self.cards.all()]
                                    },

                "favstores" : [fav.json()["storeid"] for fav in self.favstores.all()],
                # "mycarts" : [purchase_detail.json() for purchase_detail in self.purchased.all()],
                # "purchased" : [cart.json() for cart in self.carts.all()],
                # "notifications" : [notice.json() for notice in self.notifications.all()],
                }
        

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

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
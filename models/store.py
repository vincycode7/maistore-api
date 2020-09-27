from db import db
from datetime import datetime as dt
from models.models_helper import ModelsHelper
from typing import Dict, List


class StoreModel(db.Model, ModelsHelper):
    __tablename__ = "store"

    # class variable
    id = db.Column(db.Integer, primary_key=True, unique=True)
    storename = db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    country = db.Column(db.String(30))

    # merge (for sqlalchemy to link tables)
    user = db.relationship("UserModel")
    products = db.relationship("ProductModel", lazy="dynamic")
    customers = db.relationship("FavStoreModel", lazy="dynamic")
    orders = db.relationship("CartSystemModel", lazy="dynamic")
    locations = db.relationship("StorelocModel", lazy="dynamic")
    phonenos = db.relationship("StorephoneModel", lazy="dynamic")
    emails = db.relationship("StoreemailModel", lazy="dynamic")

    # set children
    _childrelations = [
        "products",
        "customers",
        "orders",
        "locations",
        "phonenos",
        "emails",
    ]

    def __init__(
        self, storename: str, user_id: int, country: str = None, created: str = None
    ):
        self.storename = storename
        self.user_id = user_id
        self.country = country
        self.created = created if created else dt.now()

    # a json representation
    def json(self) -> Dict:
        return {
            "id": self.id,
            "storename": self.storename,
            "userid": self.user_id,
            "country": self.country,
            "products": [product.json() for product in self.products.all()],
            "customers": [
                customer.json()["email"] for customer in self.customers.all()
            ],
            "phonenos": [num.json() for num in self.phonenos.all()],
            "emails": [email.json() for email in self.emails.all()],
        }

    @classmethod
    def find_all(cls) -> List["StoreModel"]:
        result = cls.query.all()
        return result

    @classmethod
    def find_by_name(cls, storename: str = None) -> "StoreModel":
        result = cls.query.filter_by(storename=storename).first()
        return result

    @classmethod
    def find_by_id(cls, storeid: int) -> "StoreModel":
        result = cls.query.filter_by(id=storeid).first()
        return result

# This table will hold the created carts

from db import db
from datetime import datetime as dt


class CartSystemModel(db.Model):
    __tablename__ = "cartsystem"

    # columns
    id = db.Column(db.Integer, primary_key=True, unique=True)
    statustime = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"), nullable=False)
    status = db.Column(db.Integer, db.ForeignKey("cartstatus.id"), nullable=False)

    # merge
    user = db.relationship("UserModel")
    products = db.relationship("CartProductModel", lazy="dynamic")

    def __init__(self, user_id, store_id, status, statustime):
        self.user_id = user_id
        self.store_id = store_id
        self.status = status
        self.statustime = statustime

    def json(self):

        return {
            "id": self.id,
            "statustime": self.statustime,
            "user_id": self.user_id,
            "store_id": self.store_id,
            "ordered_products": [product.json() for product in self.products.all()],
            "status": self.status,
        }

    def save_to_db(self):
        # connect to the database
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        result = cls.query.all()
        return result

    @classmethod
    def find_by_store_id(cls, productid=None):
        result = cls.query.filter_by(productid=productid).first()
        return result

    @classmethod
    def find_by_id(cls, id):
        result = cls.query.filter_by(id=id).first()
        return result

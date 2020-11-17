# This table will hold the created carts
from models.models_helper import *


class CartSystemModel(db.Model, ModelsHelper):
    __tablename__ = "cartsystem"

    # columns
    id = db.Column(db.Integer, primary_key=True, unique=True)
    statustime = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey("users.id"), nullable=False)
    store_id = db.Column(db.String(50), db.ForeignKey("store.id"), nullable=False)
    status = db.Column(db.Integer, db.ForeignKey("cartstatus.id"), nullable=False)

    # merge
    # user = db.relationship("UserModel")
    products = db.relationship(
        "CartProductModel",
        backref="cartsystem",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    @classmethod
    def find_by_store_id(cls, store_id=None):
        result = cls.query.filter_by(store_id=store_id).first()
        return result

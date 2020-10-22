# This table will hold the products added to a cart from a store
# Note more than one products in a cart must all be from the same store

from models.models_helper import *


class CartProductModel(db.Model, ModelsHelper):
    __tablename__ = "cartproduct"

    # columns
    id = db.Column(db.Integer, primary_key=True, unique=True)
    product_id = db.Column(db.String(50), db.ForeignKey("product.id"), nullable=False)
    store_id = db.Column(db.String(50), db.ForeignKey("store.id"), nullable=False)
    cartsystemid = db.Column(db.Integer, db.ForeignKey("cartsystem.id"), nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey("user.id"), nullable=False)
    created = db.Column(
        db.DateTime, index=False, unique=False, nullable=False, default=dt.now
    )

    @classmethod
    def find_by_productid(cls, productid=None):
        result = cls.query.filter_by(productid=productid).first()
        return result

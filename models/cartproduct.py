# This table will hold the products added to a cart from a store
# Note more than one products in a cart must all be from the same store

from db import db
from datetime import datetime as dt

class CartProductModel(db.Model):
    __tablename__ = "cartproduct"

    #columns
    id = db.Column(db.Integer, primary_key=True, unique=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"), nullable=False)
    cartsystemid = db.Column(db.Integer, db.ForeignKey("cartsystem.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created = db.Column(db.DateTime, index=False, unique=False, nullable=False)

    def __init__(self, product_id, store_id, user_id, cartsystemid, statustime, created=None):
        self.user_id = store_id,
        self.store_id = store_id
        self.user_id = user_id
        self.product_id = product_id
        self.cartsystemid = cartsystemid
        self.created = created if created else dt.now()

    def json(self):

        return {
                "id" : self.id,
                "created" : self.created,
                "user_id" : self.user_id,
                "store_id" : self.store_id,
                "product_id" : self.product_id,
                "cartsystemid " : self.cartsystemid
        }

    def save_to_db(self):
        #connect to the database
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
    def find_by_productid(cls, productid=None):
        result = cls.query.filter_by(productid=productid).first()
        return result    

    @classmethod
    def find_by_id(cls, id):
        result = cls.query.filter_by(id=id).first()
        return result    
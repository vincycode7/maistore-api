# This table will hold the list of status for a cart
from models.models_helper import *


class CartStatusModel(db.Model, ModelsHelper):
    __tablename__ = "cartstatus"

    # columns
    id = db.Column(db.Integer, primary_key=True, unique=True)
    desc = db.Column(db.String(20))

    @classmethod
    def find_by_productid(cls, product_id=None):
        result = cls.query.filter_by(product_id=product_id).first()
        return result

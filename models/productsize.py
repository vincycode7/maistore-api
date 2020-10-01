from models.models_helper import *


class ProductSizeModel(db.Model, ModelsHelper):
    __tablename__ = "productsize"

    # class variables
    id = db.Column(db.Integer, primary_key=True, unique=True)
    productid = db.Column(db.Integer, db.ForeignKey("product.id"))
    desc = db.Column(db.String(256))

    @classmethod
    def find_by_productid(cls, productid=None):
        result = cls.query.filter_by(productid=productid).first()
        return result

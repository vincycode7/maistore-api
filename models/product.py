from models.models_helper import *
from models.store import StoreModel


#helper functions
def is_avail(context):
    is_available = context.get_current_parameters()['is_available']
    quantity = context.get_current_parameters()['quantity']
    if is_available and quantity > 0: return True
    else: return False

class ProductModel(db.Model,ModelsHelper):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    productname = db.Column(db.String(40))
    price = db.Column(db.Float(precision=2))
    quantity = db.Column(db.Integer)
    desc = db.Column(db.String(200))
    productcat_id = db.Column(
        db.Integer,
        db.ForeignKey("productcat.id"),
        index=False,
        unique=False,
        nullable=False,
    )
    store_id = db.Column(
        db.Integer, db.ForeignKey("store.id"), index=False, unique=False, nullable=False
    )
    is_available = db.Column(db.Boolean, index=False, unique=False, nullable=False, default=is_avail, onupdate=is_avail)

    #merge
    reviews = db.relationship("ReviewModel", lazy="dynamic", backref="product", cascade="all, delete-orphan")
    sizes = db.relationship("ProductSizeModel", lazy="dynamic", backref="product", cascade="all, delete-orphan")
    colors = db.relationship("ProductColorModel", lazy="dynamic", backref="product", cascade="all, delete-orphan")

    @classmethod
    def find_by_name(cls, productname=None):
        result = cls.query.filter_by(productname=productname).first()
        return result

    @staticmethod
    def store_queryby_id(store_id):
        return StoreModel.find_by_id(storeid=store_id)

from db import db
from models.models_helper import ModelsHelper
from models.store import StoreModel

class ProductModel(db.Model, ModelsHelper):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    productname = db.Column(db.String(40))
    price = db.Column(db.Float(precision=2))
    quantity = db.Column(db.Integer)
    desc = db.Column(db.String(200))
    productcat_id = db.Column(db.Integer, db.ForeignKey('productcat.id'), index=False, unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"), index=False, unique=False, nullable=False)
    is_available = db.Column(db.Boolean, index=False, unique=False, nullable=False)

    productcat = db.relationship("ProductCatModel")
    store = db.relationship("StoreModel")
    reviews = db.relationship("ReviewModel", lazy="dynamic")
    sizes = db.relationship("ProductSizeModel", lazy="dynamic")
    colors = db.relationship("ProductColorModel", lazy="dynamic")

    _childrelations = ['reviews', 'sizes', 'colors']

    def __init__(self, productname, price, store_id, category, desc=None, is_available=False, quantity=0):
        self.productname = productname
        self.price = price
        self.store_id = store_id
        self.productcat_id = category
        self.quantity = quantity
        self.desc = desc
        if is_available or self.quantity > 0:
            self.is_available = True 
        else:
            self.is_available = False

    # a json representation
    def json(self):
        return  {
                    "id" : self.id,
                    "productname" : self.productname,
                    "price" : self.price,
                    "quantity" : self.quantity,
                    "store_id" : self.store_id,
                    "user_id" : self.store.user_id,
                    "is_available" : self.is_available,
                    "category_id" : self.productcat_id,
                    "desc" : self.desc,
                    "reviews" : [review.json() for review in self.reviews.all()],
                    "sizes" : [size.json() for size in self.sizes.all()],
                    "colors" : [color.json() for color in self.colors.all()]
                }

    @classmethod
    def find_all(cls):
        result = cls.query.all()
        return result    

    @classmethod
    def find_by_name(cls, productname=None):
        result = cls.query.filter_by(productname=productname).first()
        return result    

    @classmethod
    def find_by_id(cls, productid):
        result = cls.query.filter_by(id=productid).first()
        return result    

    @staticmethod
    def store_queryby_id(store_id):
        return StoreModel.find_by_id(storeid=store_id)
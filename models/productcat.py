from db import db

class ProductCatModel(db.Model):
    __tablename__ = "productcat"

    # columns
    id = db.Column(db.Integer, primary_key=True,  unique=True)
    desc = db.Column(db.String(256))

    # merge
    products = db.relationship("ProductModel", lazy="dynamic")

    def __init__(self, desc):
        self.desc = desc

    def json(self):
        return {
                    "id" : self.id,
                    "desc" : self.desc,
                    "products" : [product.json() for product in self.products.all()],
        }
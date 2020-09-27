from db import db


class ProductCatModel(db.Model):
    __tablename__ = "productcat"

    # columns
    id = db.Column(db.Integer, primary_key=True, unique=True)
    desc = db.Column(db.String(256))

    # merge
    products = db.relationship("ProductModel", lazy="dynamic")

    def __init__(self, desc):
        self.desc = desc

    def json(self):
        return {
            "id": self.id,
            "desc": self.desc,
            "products": [product.json() for product in self.products.all()],
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
    def find_by_productid(cls, productid=None):
        result = cls.query.filter_by(productid=productid).first()
        return result

    @classmethod
    def find_by_id(cls, id):
        result = cls.query.filter_by(id=id).first()
        return result

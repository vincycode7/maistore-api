from db import db

class ProductModel(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    productname = db.Column(db.String(40))
    price = db.Column(db.Float(precision=2))
    quantity = db.Column(db.Integer)
    productcat_id = db.Column(db.Integer, db.ForeignKey('productcat.id'))
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))

    # productcat = db.relationship("ProductCatModel")
    store = db.relationship("StoreModel")
    # sizes = db.relationship("ProductSizeModel", lazy="dynamic")

    def __init__(self, productname, price, store_id, category, quantity=0):
        self.productname = productname
        self.price = price
        self.store_id = store_id
        self.productcat_id = category
        self.quantity = quantity

    # a json representation
    def json(self):
        return  {
                    "id" : self.id,
                    "productname" : self.productname,
                    "price" : self.price,
                    "quantity" : self.quantity,
                    "store" : self.store
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
    def find_by_name(cls, productname=None):
        result = cls.query.filter_by(productname=productname).first()
        return result    

    @classmethod
    def find_by_id(cls, _id):
        result = cls.query.filter_by(id=id).first()
        return result    

    @classmethod
    def check_form_integrity(cls,productname, data):
        #check if form is empty
        if data == None: return {"message" : "Invalid object type, use json."}, 404

        #check if   user posted it
        #implement later

        #confirm the unique key to be same with the product route
        if productname != data['productname']:
            return {"message" : f"product {productname} does not match {data['name']} in the form"}, 404

        return False
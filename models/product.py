from db import db

class ProductModel(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(40))
    price = db.Column(db.Float(precision=2))
    quantity = db.Column(db.Integer)
    category = db.Column(db.String(40))
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))
    store = db.relationship("StoreModel")

    def __init__(self, productname, price, store_id, quantity=0, category=None):
        self.productname = productname
        self.price = price
        self.quantity = quantity
        self.category = category
        self.store_id = store_id

    # a json representation
    def json(self):
        return  {
                        "productname" : self.productname,
                        "price" : self.price,
                        "quantity" : self.quantity,
                        "category" : self.category,
                        "store" : self.store.json()
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

    @classmethod
    def instance_from_dict(cls, dict_):
        return cls(
                        productname=dict_.get('productname'), 
                        price=dict_.get('price'), 
                        quantity=dict_.get('quantity', None), 
                        category=dict_.get('category', None), 
                        store_id=dict_.get('store_id')
                   )
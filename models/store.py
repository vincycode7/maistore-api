from db import db
from datetime import datetime as dt

class StoreModel(db.Model):
    __tablename__ = "store"

    # class variable
    id = db.Column(db.Integer, primary_key=True, unique=True)
    storename = db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    country = db.Column(db.String(30), nullable=False)
    # location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    
    #merge (for sqlalchemy to link tables)
    user = db.relationship("UserModel")
    products = db.relationship("ProductModel", lazy="dynamic")
    customers = db.relationship("FavStoreModel", lazy="dynamic")
    # phonenos = db.relationship("StorephoneModel", lazy="dynamic")
    # emails = db.relationship("StoremailModel", lazy="dynamic")

    def __init__(self, storename, user_id, country, created=None, location=None):
        self.storename = storename
        self.user_id = user_id
        self.location = location
        self.country = country
        self.created = created if created else dt.now()

    # a json representation
    def json(self):
        return  {
                    "id" : self.id,
                    "storename" : self.storename,
                    "country" : self.country,
                    "products" : [product.json() for product in self.products.all()],
                    "customers" : [customer.json()["email"] for customer in self.customers.all()],
                    # "location" : self.location_id,
                    # "phonenos" : [num.json() for num in self.phonenos.all()],
                    # "emails" : [email.json() for email in self.emails.all()],
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
    def find_by_name(cls, storename=None):
        result = cls.query.filter_by(storename=storename).first()
        return result    

    @classmethod
    def find_by_id(cls, _id):
        result = cls.query.filter_by(id=id).first()
        return result    

    @classmethod
    def check_form_integrity(cls,storename, data):
        #check if form is empty
        if data == None: return {"message" : "Invalid object type, use json."}, 404

        #check if   user posted it
        #implement later

        #confirm the unique key to be same with the product route
        if storename != data['storename']:
            return {"message" : f"product {storename} does not match {data['storename']} in the form"}, 404

        return False
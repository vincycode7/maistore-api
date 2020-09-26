from db import db
from datetime import datetime as dt

class StoreModel(db.Model):
    __tablename__ = "store"

    # class variable
    id = db.Column(db.Integer, primary_key=True, unique=True)
    storename = db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    country = db.Column(db.String(30))
    
    #merge (for sqlalchemy to link tables)
    user = db.relationship("UserModel")
    products = db.relationship("ProductModel", lazy="dynamic")
    customers = db.relationship("FavStoreModel", lazy="dynamic")
    orders = db.relationship("CartSystemModel", lazy="dynamic")
    locations = db.relationship("StorelocModel", lazy="dynamic")
    phonenos = db.relationship("StorephoneModel", lazy="dynamic")
    emails = db.relationship("StoreemailModel", lazy="dynamic")

    def __init__(self, storename, user_id, country=None, created=None):
        self.storename = storename
        self.user_id = user_id
        self.country = country
        self.created = created if created else dt.now()

    # a json representation
    def json(self):
        return  {
                    "id" : self.id,
                    "storename" : self.storename,
                    "userid" : self.user_id,
                    "country" : self.country,
                    "products" : [product.json() for product in self.products.all()],
                    "customers" : [customer.json()["email"] for customer in self.customers.all()],
                    "phonenos" : [num.json() for num in self.phonenos.all()],
                    "emails" : [email.json() for email in self.emails.all()],
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
    def find_by_id(cls, storeid):
        result = cls.query.filter_by(id=storeid).first()
        return result    
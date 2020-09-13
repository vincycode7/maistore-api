#import packages
from db import db

#class to create user and get user
class UserModel(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    email = db.Column(db.String(100))
    stores = db.relationship("StoreModel", lazy="dynamic")

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    # a json representation
    def json(self):
        return {
                "id" : self.id,
                "username" : self.username,
                "password" : self.password,
                "email" : self.email,
                "stores" : [store.json() for store in self.stores.all()]
                }
        

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        results = cls.query.all()  #the comma is required because it expects a tuple
        return results 

    @classmethod
    def find_by_username(cls, username=None):
        result = cls.query.filter_by(username=username).first()
        return result 

    @classmethod
    def find_by_email(cls, email=None):
        result = cls.query.filter_by(email=email).first()
        return result 

    @classmethod
    def find_by_id(cls, id):
        result = cls.query.filter_by(id=id).first()
        return result 

    @classmethod
    def check_form_integrity(cls,username=None, data=None):
        #check if form is empty
        if data == None: return {"message" : "Invalid object type, use json."}, 404

        #confirm the unique key to be same with the product route
        if username != data['username']:
            return {"message" : f"user {username} does not match {data['username']} in the form"}, 40
        #implement later

        return False

    @classmethod
    def instance_from_dict(cls, dict_):
        return cls(
                        username=dict_.get('username'), 
                        password=dict_.get('password'), 
                        email=dict_.get('email')
                   )
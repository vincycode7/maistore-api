from db import db

class StoreModel(db.Model):
    __tablename__ = "store"

    id = db.Column(db.Integer, primary_key=True)
    storename = db.Column(db.String(40))
    userid = db.Column(db.String(40))
    location = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("UserModel")
    products = db.relationship("ProductModel", lazy="dynamic")

    def __init__(self, storename, user_id, location=None):
        self.storename = storename
        self.user_id = user_id
        self.location = location

    # a json representation
    def json(self):
        return  {
                    "id" : self.id,
                    "storename" : self.storename,
                    "user" : self.user.json(),
                    "products" : [product.json() for product in self.products.all()]
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

    @classmethod
    def instance_from_dict(cls, dict_):
        return cls(
                        storename=dict_.get('storename'), 
                        user_id=dict_.get('user_id'), 
                        location=dict_.get('location', None), 
                   )
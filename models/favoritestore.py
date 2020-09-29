from db import db


class FavStoreModel(db.Model):

    __tablename__ = "favstore"

    # class variable
    id = db.Column(db.Integer, primary_key=True, unique=True)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # merge (for sqlalchemy to link tables)
    user = db.relationship("UserModel")
    store = db.relationship("StoreModel")

    def __init__(self, store_id, user_id):
        self.store_id = store_id
        self.user_id = user_id

    # a json representation
    def json(self):
        return {"id": self.id, "storeid": self.store.id, "user": self.user.email}

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
    def find_by_store_id(cls, store_id=None):
        result = cls.query.filter_by(
            store_id=store_id,
        ).first()
        return result

    @classmethod
    def find_by_user_id(cls, user_id=None):
        result = cls.query.filter_by(user_id=user_id).first()
        return result

    @classmethod
    def find_by_id(cls, _id):
        result = cls.query.filter_by(id=id).first()
        return result

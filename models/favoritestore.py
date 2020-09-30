from models.models_helper import *

class FavStoreModel(db.Model,ModelsHelper):
    __tablename__ = "favstore"

    # class variable
    id = db.Column(db.Integer, primary_key=True, unique=True)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


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
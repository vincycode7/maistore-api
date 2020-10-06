from models.models_helper import *


class LocationModel(db.Model, ModelsHelper):
    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    address = db.Column(db.String(300))
    store_id = db.Column(db.String(50), db.ForeignKey("store.id"))

    @classmethod
    def find_by_store_id(cls, store_id=None):
        result = cls.query.filter_by(
            store_id=store_id,
        ).first()
        return result

from models.models_helper import *

class StorephoneModel(db.Model,ModelsHelper):
    __tablename__ = "storephone"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))
    store_phoneno = db.Column(db.String(300))
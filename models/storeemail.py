from models.models_helper import *

class StoreemailModel(db.Model,ModelsHelper):
    __tablename__ = "storemail"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))
    store_mail = db.Column(db.String(300))
from models.models_helper import *

class StorelocModel(db.Model,ModelsHelper):

    __tablename__ = "storelocation"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))
    store_address = db.Column(db.String(300))
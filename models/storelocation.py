from db import db


class StorelocModel(db.Model):

    __tablename__ = "storelocation"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))
    store_address = db.Column(db.String(300))

    def __init__(self, store_id, store_address):
        self.store_id = store_id
        self.store_address = store_address

    def json(self):
        return {
            "id": self.id,
            "store_id": self.store_id,
            "store_address": self.store_address,
        }

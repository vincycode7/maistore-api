from db import db


class StorephoneModel(db.Model):
    __tablename__ = "storephone"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))
    store_phoneno = db.Column(db.String(300))

    def __init__(self, store_id, store_phoneno):
        self.store_id = store_id
        self.store_address = store_phoneno

    def json(self):
        return {
            "id": self.id,
            "store_id": self.store_id,
            "store_address": self.store_phoneno,
        }

from db import db


class StoreemailModel(db.Model):
    __tablename__ = "storemail"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))
    store_mail = db.Column(db.String(300))

    def __init__(self, store_id, store_mail):
        self.store_id = store_id
        self.store_mail = store_mail

    def json(self):
        return {"id": self.id, "store_id": self.store_id, "store_mail": self.store_mail}

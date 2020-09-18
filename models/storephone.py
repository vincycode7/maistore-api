from db import db

class StorephoneModel(db.Model):
    id = db.Column(db.Integer)
    store_id = db.Column(db.Integer, db.ForiegnKey("store.id"))
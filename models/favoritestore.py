from db import db

class FavstoreModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForiegnKey("user.id"))
    store_id = db.Column(db.Integer, db.ForiegnKey("store.id"))
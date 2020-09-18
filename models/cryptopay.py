from db import db

class CryptopayModel(db.Model):
    __tablename__ = "cryptopay"

    id = db.Column(db.Integer, primary_key=True)
    paymenttype = db.Column(db.Integer)
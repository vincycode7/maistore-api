from db import db

class BankpayModel(db.Model):
    __tablename__ = "bankpay"

    id = db.Column(db.Integer, primary_key=True)
    paymenttype = db.Column(db.Integer)
from db import db

class PaymethodModel(db.Model):
    __tablename__ = "paymethod"

    id = db.Column(db.Integer, primary_key=True)
    user_id = 
    paymenttype = db.Column(db.Integer)
from db import db

# class PaymentModel(db.Model):
#     __tablename__ = "payment"

#     id = db.Column(db.Integer)
#     status_code_id = db.Column(db.Integer, db.ForeignKey("paystatus.id"))
#     purchaser_id = db.Column(db.Integer, db.ForeignKey("user.id"))
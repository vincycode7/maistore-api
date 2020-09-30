from models.models_helper import *

class PaymentModel(db.Model,ModelsHelper):
    __tablename__ = "payment"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    status_code_id = db.Column(db.Integer, db.ForeignKey("paystatus.id"))
    purchaser_id = db.Column(db.Integer, db.ForeignKey("user.id"))

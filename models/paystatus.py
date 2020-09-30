from models.models_helper import *

class PaystatusModel(db.Model,ModelsHelper):
    __tablename__ = "paystatus"

    id = db.Column(db.Integer, primary_key=True)
    paymenttype = db.Column(db.Integer)

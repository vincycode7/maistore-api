from models.models_helper import *

# The bank payment type. Each user can have multiple bank payment type
#
class CardpayModel(db.Model, ModelsHelper):
    __tablename__ = "cardpay"

    # class variables
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey("users.id"))
    card_num = db.Column(db.String(256))
    card_cvv = db.Column(db.String(3))
    card_exp = db.Column(db.DateTime)
    created = db.Column(
        db.DateTime, index=False, unique=False, nullable=False, default=dt.now
    )

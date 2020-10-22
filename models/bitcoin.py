from db import db
from models.models_helper import ModelsHelper

# The crypto payment type. Each user can have multiple crypto payment type
#
class BitcoinPayModel(db.Model, ModelsHelper):
    __tablename__ = "bitcoin"

    # class variables
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.String(50), db.ForeignKey("user.id"))
    wallet_address = db.Column(db.String(256))

from models.models_helper import *

# Admin will set this -- so users can pick from this
# This is like so in case more payment system comes in future

class PaytypeModel(db.Model,ModelsHelper):
    __tablename__ = "paytype"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    desc = db.Column(db.String(30))

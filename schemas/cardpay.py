from ma import ma
from models.cardpay import CardpayModel

class CardpaySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CardpayModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True

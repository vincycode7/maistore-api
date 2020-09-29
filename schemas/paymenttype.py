from ma import ma
from models.paymenttype import PaytypeModel

class PaytypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PaytypeModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True
from ma import ma
from models.payment import PaymentModel

class PaymentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PaymentModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True
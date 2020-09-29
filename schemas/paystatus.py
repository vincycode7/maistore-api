from ma import ma
from models.paystatus import PaystatusModel

class PaystatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PaystatusModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True
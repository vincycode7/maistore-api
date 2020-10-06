from ma import ma
from models.bitcoin import BitcoinPayModel


class BitcoinPaySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BitcoinPayModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True

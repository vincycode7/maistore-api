from ma import ma
from models.storeemail import StoreemailModel

class StoreemailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StoreemailModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True

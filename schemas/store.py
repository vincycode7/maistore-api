from ma import ma
from models.store import StoreModel

class StoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StoreModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True
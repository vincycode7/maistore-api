from ma import ma
from models.storelocation import StorelocModel

class StorelocSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StorelocModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True

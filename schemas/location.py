from ma import ma
from models.location import LocationModel


class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LocationModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True

from ma import ma
from models.ratingtype import RatingTypeModel


class RatingTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RatingTypeModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True

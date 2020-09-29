from ma import ma
from models.review import ReviewModel

class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ReviewModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True
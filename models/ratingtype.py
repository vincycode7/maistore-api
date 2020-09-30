from models.models_helper import *


class RatingTypeModel(db.Model,ModelsHelper):
    __tablename__ = "ratingtype"

    # class variables
    id = db.Column(db.Integer, primary_key=True, unique=True)
    desc = db.Column(db.String(256))

    # merge
    reviews = db.relationship("ReviewModel", lazy="dynamic", backref="ratingtype", cascade="all, delete-orphan")
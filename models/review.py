from models.models_helper import *


class ReviewModel(db.Model, ModelsHelper):
    __tablename__ = "review"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    review = db.Column(db.String(400))
    product_id = db.Column(
        db.String(50),
        db.ForeignKey("product.id"),
        index=False,
        unique=False,
        nullable=False,
    )
    store_id = db.Column(
        db.String(50),
        db.ForeignKey("store.id"),
        index=False,
        unique=False,
        nullable=False,
    )
    user_id = db.Column(
        db.String(50),
        db.ForeignKey("user.id"),
        index=False,
        unique=False,
        nullable=False,
    )
    product_rating = db.Column(
        db.Integer, db.ForeignKey("ratingtype.id"), index=False, unique=False
    )

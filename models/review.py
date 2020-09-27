from db import db


class ReviewModel(db.Model):
    __tablename__ = "review"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    review = db.Column(db.String(400))
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        index=False,
        unique=False,
        nullable=False,
    )
    store_id = db.Column(
        db.Integer, db.ForeignKey("store.id"), index=False, unique=False, nullable=False
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), index=False, unique=False, nullable=False
    )
    product_rating = db.Column(
        db.Integer, db.ForeignKey("ratingtype.id"), index=False, unique=False
    )

    def __init__(self, store_id, product_id, user_id, review=None, product_rating=None):
        self.store_id = store_id
        self.product_id = product_id
        self.user_id = user_id
        self.review = review
        self.product_rating = product_rating

    # a json representation
    def json(self):
        return {
            "id": self.id,
            "productid": self.product_id,
            "productrating": self.product_rating,
            "store_id": self.store_id,
            "review": self.review,
        }

    def save_to_db(self):
        # connect to the database
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        result = cls.query.all()
        return result

    @classmethod
    def find_by_id(cls, reviewid):
        result = cls.query.filter_by(id=reviewid).first()
        return result

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.review import ReviewModel

class ReviewList(Resource):
    def get(self):
        reviews = ReviewModel.find_all()
        if reviews: return {"reviews" : [ review.json() for review in reviews]},201
        return {"message" : 'Reviews not found'}, 400
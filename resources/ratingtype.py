import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.ratingtype import RatingTypeModel

#class to list all user
class RatingTypeList(Resource):
    def get(self):        
        ratings = RatingTypeModel.find_all()
        if ratings: return {"ratings" : [ rating.json() for rating in ratings]},201
        return {"message" : 'Ratings not found'}, 400
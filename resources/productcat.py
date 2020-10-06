import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.productcat import ProductCatModel

# class to list all user
class ProductCatList(Resource):
    @jwt_required
    def get(self):
        productcats = ProductCatModel.find_all()
        if productcats:
            return {"users": [productcat.json() for productcat in productcats]}, 201
        return {"message": "Item not found"}, 400

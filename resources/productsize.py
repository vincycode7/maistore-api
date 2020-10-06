from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.productsize import ProductSizeModel

# class to list all user
class ProductSizeList(Resource):
    @jwt_required
    def get(self):
        productsizes = ProductSizeModel.find_all()
        if productsizes:
            return {
                "productsize": [productsize.json() for productsize in productsizes]
            }, 201
        return {"message": "Item not found"}, 400

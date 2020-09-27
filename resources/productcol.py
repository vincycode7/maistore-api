from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.productcol import ProductColorModel

#class to list all ProductColors
class ProductColorList(Resource):
    @jwt_required
    def get(self):        
        productcolors = ProductColorModel.find_all()
        if productcolors: return {"productcolors" : [ productcolor.json() for productcolor in productcolors]},201
        return {"message" : 'Item not found'}, 400
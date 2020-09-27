from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.cartproduct import CartProductModel

class CartProductList(Resource):
    @jwt_required
    def get(self):
        cartproducts = CartProductModel.find_all()
        if cartproducts: return {"cartproducts" : [ cartproduct.json() for cartproduct in cartproducts]},201
        return {"message" : 'Item not found'}, 400
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.cartsystem import CartSystemModel

class CartSystemList(Resource):
    @jwt_required()
    def get(self):
        cartsystems = CartSystemModel.find_all()
        if cartsystems: return {"cartsystems" : [ cartsystem.json() for cartsystem in cartsystems]},201
        return {"message" : 'Item not found'}, 400
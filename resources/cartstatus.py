from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.cartstatus import CartStatusModel

class CartStatusList(Resource):
    @jwt_required()
    def get(self):
        cartstatuses = CartStatusModel.find_all()
        if cartstatuses: return {"cartstatuses" : [ cartstatus.json() for cartstatus in cartstatuses]},201
        return {"message" : 'Item not found'}, 400
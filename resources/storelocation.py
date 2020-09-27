from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.storelocation import StorelocModel

class StorelocList(Resource):
    @jwt_required
    def get(self):
        storeslocations = StorelocModel.find_all()
        if storeslocations: return {"storeslocations" : [ storelocation.json() for storelocation in storeslocations]},201
        return {"message" : 'Item not found'}, 400
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.storephone import StorephoneModel

class StorephoneList(Resource):
    @jwt_required
    def get(self):
        storesphones = StorephoneModel.find_all()
        if storesphones: return {"storephone" : [ storephone.json() for storephone in storesphones]},201
        return {"message" : 'Item not found'}, 400
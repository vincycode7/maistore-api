from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.storeemail import StoreemailModel

class StoreemailList(Resource):
    @jwt_required()
    def get(self):
        storesemails = StoreemailModel.find_all()
        if storesemails: return {"storesemails" : [ storeemail.json() for storeemail in storesemails]},201
        return {"message" : 'Item not found'}, 400
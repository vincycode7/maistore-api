from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.bitcoin import BitcoinPayModel

class BitcoinList(Resource):
    @jwt_required
    def get(self):        
        bitcoins = BitcoinPayModel.find_all()
        if bitcoins: return {"bitcoins" : [ bitcoin.json() for bitcoin in bitcoins]},201
        return {"message" : 'Item not found'}, 400
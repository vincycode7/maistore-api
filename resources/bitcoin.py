from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.bitcoin import BitcoinPayModel


class BitcoinList(Resource):
    @jwt_required
    def get(self):
        bitcoins = BitcoinPayModel.find_all()
        if bitcoins:
            return {"message": gettext("work_in_progress")}, 400
            # return {"bitcoins": [bitcoin.json() for bitcoin in bitcoins]}, 201
        return {"message": gettext("bitcoin_not_found")}, 404

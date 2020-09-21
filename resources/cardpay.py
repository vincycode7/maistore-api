from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.cardpay import CardpayModel

class CardPayList(Resource):
    @jwt_required()
    def get(self):
        cardpays = CardpayModel.find_all()
        if cardpays: return {"cardpays" : [ cardpay.json() for cardpay in cardpays]}, 201
        return {"message" : 'Item not found'}, 400
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.cardpay import CardpayModel


class CardPayList(Resource):
    @jwt_required
    def get(self):
        cardpays = CardpayModel.find_all()
        if cardpays:
            return {"message": gettext("work_in_progress")}, 400
            # return {"cardpays": [cardpay.json() for cardpay in cardpays]}, 201
        return {"message": gettext("cardpay_not_found")}, 404

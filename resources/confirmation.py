import traceback
from time import time

from flask_restful import Resource
from flask import make_response, render_template

from models.user import UserModel
from error_messages import *
from schemas.confirmation import ConfirmationSchema
from libs.mailer import MailerException

confirimation_schema = ConfirmationSchema()
class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str):
        """ Return confirmation HTML """
        confirmation = ConfirmationModel.find_by_id(id=confirmation_id)

        if not confirmation:
            return {"message" : NOT_FOUND.format("user confirmation")}, 404

        elif confirmation.expired:
            return {"message" : EXPIRED.format("user confirmation")}, 400
        
        elif confirmation.confirmed:
            return {"message" : ALREADY_CONFIRMED.format("user confirmation id", confirmation.id)}, 400

        try:
            confirmation.confirmed = True
            confirmation.save_to_db()
        except Exception as e:
            print(e)
            return ERROR_WHILE.format("confirming user"), 500

        headers = {"Content-Type": "text/html"}
        return make_response(
            render_template("confirmation_page.html", email=confirmation.user.email), 200, headers
        )

class ConfirmationByUser(Resource):
    @classmethod
    def get(cls, user_id:int):
        """ Returns confirmations for a given user. Use for testing """
        user = UserModel.find_by_id(id=user_id)
        if not user:
            return {"message" : NOT_FOUND.format("user")}, 404

        return {
                    "current_time" : int(time()),
                    "confirmations" : [
                                        confirimation_schema.dump(each)
                                        for each in user.confirmation.order_by(ConfirmationModel.expire_at)
                                        ], 
                }, 200
    @classmethod
    def post(cls, user_id:int):
        """ Resend confirmation email """
        user = UserModel.find_by_id(id=user_id)

        if not user:
            return {"message" : NOT_FOUND.format("user id")}, 404
        
        try:
            confirimation = user.most_recent_confirmation
            if confirimation:
                if confirimation.confirmed:
                    return {"message" : ALREADY_CONFIRMED.format("user confirmation id", confirmation.id)}, 400
                confirimation.forced_to_expire()
                new_confirmation = Confirmation(user_id)
                new_confirmation.save_to_db()
                user.send_confirmation_email()

                return {"message" : CONFIRMATION_RESEND_SUCCESSFUL}, 201
        except MailerException as e:
            return {"message" : str(e)}, 500
        
        except:
            traceback.print_exc()
            return {"message" : CONFIRMATION_RESEND_FAILED}, 500
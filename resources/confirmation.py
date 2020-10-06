import traceback
from time import time

from flask_restful import Resource
from flask import make_response, render_template
from flask_jwt_extended import jwt_required, get_jwt_claims

from models.user import UserModel
from db import db
from error_messages import *
from schemas.confirmation import ConfirmationSchema
from models.confirmation import ConfirmationModel
from libs.mailer import MailerException

confirmation_schema = ConfirmationSchema()
confirimation_schema_many = ConfirmationSchema(many=True)


# use to confirm user
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

# use to view or resend confirmations
class ConfirmationByUser(Resource):
    @classmethod
    # @jwt_required
    def get(cls, user_id:int):
        """ Returns confirmations for a given user. Use for testing """
        claim = get_jwt_claims()
        if not claim or not claim["is_admin"]:
            return {
                "message": ADMIN_PRIVILEDGE_REQUIRED.format("to get user confirmations")
            }, 401

        user = UserModel.find_by_id(id=user_id)
        if not user:
            return {"message" : NOT_FOUND.format("user")}, 404
        return ({
                    "current_time" : int(time()),
                    "confirmations" : [
                                        confirmation_schema.dump(each)
                                        for each in user.confirmation.order_by(ConfirmationModel.expire_at)
                                        ], 
                }, 200)
        return {"message" : "testing"}, 200

    @classmethod
    def post(cls, user_id:int=None):
        """ Resend confirmation email """
        user = UserModel.find_by_id(id=user_id)

        if not user:
            return {"message" : NOT_FOUND.format("user id")}, 404
        
        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                if confirmation.confirmed:
                    return {"message" : ALREADY_CONFIRMED.format("user confirmation id", confirmation.id)}, 400
                confirmation.force_to_expire()
                new_confirmation = ConfirmationModel(user_id)
                new_confirmation.save_to_db()
                user.send_confirmation_email()

                return {"message" : CONFIRMATION_RESEND_SUCCESSFUL}, 201
        except MailerException as e:
            return {"message" : str(e)}, 500
        
        except:
            traceback.print_exc()
            return {"message" : CONFIRMATION_RESEND_FAILED}, 500
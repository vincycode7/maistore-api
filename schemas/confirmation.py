from models.confirmation import ConfirmationModel
from marshmallow import pre_dump
from ma import ma

class ConfirmationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ConfirmationModel
        load_only = ("user_id",)
        dump_only = ("id", "expired_at", "confirmed", )
        include_fk = True
        include_relationships = True
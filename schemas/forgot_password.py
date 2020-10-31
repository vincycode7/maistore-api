from models.forgot_password import ForgotPasswordModel
from marshmallow import pre_dump
from ma import ma


class ForgotPasswordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ForgotPasswordModel
        load_only = ("user_id",)
        dump_only = (
            "id",
            "expired_at",
            "used",
        )
        include_fk = True
        include_relationships = True
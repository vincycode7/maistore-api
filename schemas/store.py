from ma import ma
from models.store import StoreModel
from schemas.user import UserSchema
from marshmallow_sqlalchemy import fields


class StoreSchema(ma.SQLAlchemyAutoSchema):
    user = fields.Nested(
        lambda: UserSchema(only=("id", "firstname", "middlename", "lastname"))
    )

    class Meta:
        model = StoreModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True

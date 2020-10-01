from ma import ma
from marshmallow_sqlalchemy import fields
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    stores = fields.Nested("StoreSchema", many=True, exclude=("user",))

    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = (
            "id",
            "activated",
        )
        include_fk = True
        include_relationships = True

from ma import ma
from models.store import StoreModel
from schemas.users import UserSchema
from marshmallow_sqlalchemy import fields


class StoreSchema(ma.SQLAlchemyAutoSchema):
    users = fields.Nested(
        lambda: UserSchema(only=("id", "firstname", "middlename", "lastname"))
    )

    products = fields.Nested("ProductSchema", many=True, exclude=("store",))

    class Meta:
        model = StoreModel
        # load_only = ("user_id",)
        dump_only = ("id",)
        exclude = ("avatar",)
        include_fk = True
        include_relationships = True

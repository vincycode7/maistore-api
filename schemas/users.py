from ma import ma
from marshmallow_sqlalchemy import fields
from marshmallow import pre_dump
from models.users import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    stores = fields.Nested("StoreSchema", many=True, exclude=("users",))

    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = (
            "id",
            "confirmation",
        )
        include_fk = True
        include_relationships = True

    @pre_dump
    def _pre_dump(self, users: UserModel, **kwargs):
        users.confirmation = [users.most_recent_confirmation]
        return users

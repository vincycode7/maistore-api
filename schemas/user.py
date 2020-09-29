from ma import ma
from models.user import UserModel

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True
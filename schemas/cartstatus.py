from ma import ma
from models.cartstatus import CartStatusModel


class CartStatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CartStatusModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True

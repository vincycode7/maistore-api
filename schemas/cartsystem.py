from ma import ma
from models.cartsystem import CartSystemModel


class CartSystemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CartSystemModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True

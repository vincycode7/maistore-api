from ma import ma
from models.product import ProductModel


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True

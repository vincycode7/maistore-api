from ma import ma
from models.productcat import ProductCatModel

from models.product import ProductModel
from schemas.product import ProductSchema

class ProductCatSchema(ma.SQLAlchemyAutoSchema):
    products = ma.Nested(ProductSchema, many=True)
    class Meta:
        model = ProductCatModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
from ma import ma
from marshmallow_sqlalchemy import fields
from models.productcol import ProductColorModel
from schemas.product import ProductSchema
from schemas.colors import ColorsSchema


class ProductColorSchema(ma.SQLAlchemyAutoSchema):
    product = fields.Nested(lambda: ProductSchema(only=("id", "productname", "store")))
    colors = fields.Nested(lambda: ColorsSchema(only=("desc", "id")))

    class Meta:
        model = ProductColorModel
        load_only = ("color_id", "product_id")
        dump_only = ("id",)
        include_fk = True
        include_relationships = True

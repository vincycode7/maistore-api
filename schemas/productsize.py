from ma import ma
from models.productsize import ProductSizeModel
from schemas.productcat import ProductCatSchema
from schemas.productsubcat import ProductSubCatSchema
from marshmallow_sqlalchemy import fields


class ProductSizeSchema(ma.SQLAlchemyAutoSchema):
    productcat = fields.Nested(lambda: ProductCatSchema(only=("desc", "id")))
    productsubcat = fields.Nested(lambda: ProductSubCatSchema(only=("desc", "id")))

    class Meta:
        model = ProductSizeModel
        load_only = ("productsubcat_id", "productcat_id")
        dump_only = ("id",)
        include_fk = True
        include_relationships = True

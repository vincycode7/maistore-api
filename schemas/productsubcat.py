from ma import ma
from models.productsubcat import ProductSubCatModel
from schemas.productcat import ProductCatSchema
from marshmallow_sqlalchemy import fields


class ProductSubCatSchema(ma.SQLAlchemyAutoSchema):
    productcat = fields.Nested(lambda: ProductCatSchema(only=("desc", "id")))
    productsize = fields.Nested(
        "ProductSizeSchema",
        many=True,
        exclude=(
            "productcat",
            "products",
            "productcatid",
            "productsubcat",
        ),
    )

    class Meta:
        model = ProductSubCatModel
        load_only = ("categorycatid",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True

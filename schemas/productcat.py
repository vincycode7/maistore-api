from ma import ma
from models.productcat import ProductCatModel
from marshmallow_sqlalchemy import fields


class ProductCatSchema(ma.SQLAlchemyAutoSchema):
    productsubcat = fields.Nested(
        "ProductSubCatSchema",
        many=True,
        exclude=(
            "productcat",
            "products",
            "productsize",
        ),
    )
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
        model = ProductCatModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True

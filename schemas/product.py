from ma import ma
from marshmallow_sqlalchemy import fields
from schemas.productsize import ProductSizeSchema
from schemas.productcat import ProductCatSchema
from schemas.productsubcat import ProductSubCatSchema

# from schemas.productcol import ProductColorSchema
# from schemas.colors import ColorsSchema
from schemas.store import StoreSchema
from models.product import ProductModel


class ProductSchema(ma.SQLAlchemyAutoSchema):
    # to create fields to dump
    # Note: variable name must the the same as name
    # in backref
    store = fields.Nested(lambda: StoreSchema(only=("storename","user", "id",)))
    productsize = fields.Nested(lambda: ProductSizeSchema(only=("desc","id")))
    productcat = fields.Nested(lambda: ProductCatSchema(only=("desc","id")))
    productsubcat = fields.Nested(lambda: ProductSubCatSchema(only=("desc","id")))
    productcol = fields.Nested(
        "ProductColorSchema",
        many=True,
        exclude=(
            "product",
            "productid",
        ),
    )

    class Meta:
        model = ProductModel
        load_only = ("productcat_id","store_id","productsubcat_id","size_id",)
        dump_only = ("is_available")
        include_fk = True
        include_relationships = True

from ma import ma
from models.productcat import ProductCatModel

class ProductCatSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductCatModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True
from ma import ma
from models.productsize import ProductSizeModel

class ProductSizeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductSizeModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True

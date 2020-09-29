from ma import ma
from models.productcol import ProductColorModel

class ProductColorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductColorModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True

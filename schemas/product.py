from ma import ma
from models.product import ProductModel

# dependencies
from models.productcat import ProductCatModel
from schemas.productcat import ProductCatSchema

from models.review import ReviewModel
from schemas.review import ReviewSchema

from models.productsize import ProductSizeModel
from schemas.productsize import ProductSizeSchema

from models.productcol import ProductColorModel
from schemas.productcol import ProductColorSchema

from models.store import StoreModel
from schemas.store import StoreSchema

class ProductSchema(ma.SQLAlchemyAutoSchema):
    productcat = ma.Nested(ProductCatSchema, many=False)
    store = ma.Nested(StoreSchema, many=False)
    reviews = ma.Nested(ReviewSchema, many=True)
    sizes = ma.Nested(ProductSizeSchema, many=True)
    colors = ma.Nested(ProductColorSchema, many=True)
    class Meta:
        model = ProductModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
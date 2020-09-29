from ma import ma
from models.store import StoreModel

#dependencies
from models.product import ProductModel
from schemas.product import ProductSchema

from models.user import UserModel
from schemas.user import UserSchema

from models.favoritestore import FavStoreModel
from schemas.favoritestore import FavStoreSchema

from models.cartsystem import CartSystemModel
from schemas.cartsystem import CartSystemSchema

from models.storelocation import StorelocModel
from schemas.storelocation import StorelocSchema

from models.storephone import StorephoneModel
from schemas.storephone import StorephoneSchema

from models.storeemail import StoreemailModel
from schemas.storeemail import StoreemailSchema



class StoreSchema(ma.SQLAlchemyAutoSchema):
    user = ma.Nested(UserSchema, many=False)
    products = ma.Nested(ProductSchema, many=True)
    customers = ma.Nested(FavStoreSchema, many=True)
    orders = ma.Nested(CartSystemSchema, many=True)
    locations = ma.Nested(StorelocSchema, many=True)
    phonenos = ma.Nested(StorephoneSchema, many=True)
    emails = ma.Nested(StoreemailSchema, many=True)

    class Meta:
        model = StoreModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
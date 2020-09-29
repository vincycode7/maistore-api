from ma import ma
from models.user import UserModel

# dependencies
from models.store import StoreModel
from schemas.store import StoreSchema
from models.bitcoin import BitcoinPayModel
from schemas.bitcoin import BitcoinPaySchema
from models.cardpay import CardpayModel
from schemas.cardpay import CardpaySchema
from models.favoritestore import FavStoreModel
from schemas.favoritestore import FavStoreSchema
from models.cartsystem import CartSystemModel
from schemas.cartsystem import CartSystemSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    stores = ma.Nested(StoreSchema, many=True)
    bitcoins = ma.Nested(BitcoinPaySchema, many=True)
    cards = ma.Nested(CardpaySchema, many=True)
    favstores = ma.Nested(FavStoreSchema, many=True)
    carts = ma.Nested(CartSystemSchema, many=True)
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
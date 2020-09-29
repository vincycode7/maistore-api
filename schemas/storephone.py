from ma import ma
from models.storephone import StorephoneModel
# from schemas.user import UserSchema
# from schemas.bitcoin import BitcoinPaySchema
# from schemas.cardpay import CardpaySchema
# from schemas.favoritestore import FavStoreSchema
# from schemas.cartsystem import CartSystemSchema

# reviews = db.relationship("ReviewModel", lazy="dynamic", cascade="all, delete-orphan")
# sizes = db.relationship("ProductSizeModel", lazy="dynamic", cascade="all, delete-orphan")
# colors = db.relationship("ProductColorModel", lazy="dynamic", cascade="all, delete-orphan")

class StorephoneSchema(ma.SQLAlchemyAutoSchema):
    # stores = ma.Nested(StoreSchema, many=True)
    # bitcoins = ma.Nested(BitcoinPaySchema, many=True)
    # cards = ma.Nested(CardpaySchema, many=True)
    # favstores = ma.Nested(FavStoreSchema, many=True)
    # carts = ma.Nested(CartSystemSchema, many=True)
    class Meta:
        model = StorephoneModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True

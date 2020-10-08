from resources.user import (User,UserList,UserRegister,UserLogin,TokenRefresh,UserLogout,)
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.store import Store, StoreList
from resources.product import Product, ProductList
from resources.productcat import ProductCatList
from resources.productsize import ProductSizeList
from resources.productcol import ProductColorList
from resources.bitcoin import BitcoinList
from resources.cardpay import CardPayList
from resources.favoritestore import FavStoreList
from resources.cartstatus import CartStatusList
from resources.cartsystem import CartSystemList
from resources.cartproduct import CartProductList
from resources.storeemail import StoreemailList
from resources.storelocation import StorelocList
from resources.storephone import StorephoneList
from resources.ratingtype import RatingTypeList
from resources.review import ReviewList

api_version = "/api/v1"
route_path = [
    [TokenRefresh, [api_version+"/refresh"]],  # https://mistore.com/refresh
    [UserRegister, [api_version+"/register"]],  # https://mistore.com/register
    [Confirmation, [api_version+"/user_confirmation/<string:confirmation_id>"]],  # https://mistore.com/user_confirmation/1
    [ConfirmationByUser, [api_version+"/confirmation/user/<string:user_id>"]],  # https://mistore.com/confirmation/user/1
    [UserLogin, [api_version+"/login"]],  # https://mistore.com/register
    [UserLogout, [api_version+"/logout"]],  # https://mistore.com/register
    [User, [api_version+"/user/<string:userid>"]],  # https://mistore.com/user/1
    [UserList, [api_version+"/users"]],  # https://mistore.com/users
    [Store, [api_version+"/store/<string:storeid>", api_version+"/store"]],  # https://maistore.com/store/1
    [StoreList, [api_version+"/stores"]],  # https://maistore.com/store
    [ProductList, [api_version+"/products"]],  # https://mistore.com/product
    [
        Product,
        [api_version+"/product/<int:productid>", api_version+"/product"],
    ],  # https://mistore.com/product/bags
]

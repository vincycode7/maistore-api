from resources.productsubcat import ProductSubCatList, ProductSubCat
from resources.user import (
    User,
    UserList,
    UserRegister,
    UserLogin,
    TokenRefresh,
    UserLogout,
)
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.store import Store, StoreList
from resources.product import Product, ProductList
from resources.productcat import ProductCatList, ProductCat
from resources.productsize import ProductSizeList, ProductSize
from resources.productcol import ProductColorList, ProductColor
from resources.colors import ColorList, Color
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
    [TokenRefresh, [api_version + "/refresh"]],  # https://mistore.com/refresh
    [UserRegister, [api_version + "/register"]],  # https://mistore.com/register
    [
        Confirmation,
        [api_version + "/user_confirmation/<string:confirmation_id>"],
    ],  # https://mistore.com/user_confirmation/1
    [
        ConfirmationByUser,
        [api_version + "/confirmation/user/<string:user_id>"],
    ],  # https://mistore.com/confirmation/user/1
    [UserLogin, [api_version + "/login"]],  # https://mistore.com/register
    [UserLogout, [api_version + "/logout"]],  # https://mistore.com/register
    [User, [api_version + "/user/<string:userid>"]],  # https://mistore.com/user/1
    [UserList, [api_version + "/users"]],  # https://mistore.com/users
    [
        Store,
        [api_version + "/store/<string:storeid>", api_version + "/store"],
    ],  # https://maistore.com/store/1
    [StoreList, [api_version + "/stores"]],  # https://maistore.com/store
    [ProductList, [api_version + "/products"]],  # https://maistore.com/product
    [
        Product,
        [api_version + "/product/<string:productid>", api_version + "/product"],
    ],  # https://mistore.com/product/bags
    [
        ProductCatList,
        [api_version + "/productcats"],
    ],  # https://maistore.com/productcats
    [
        ProductCat,
        [api_version + "/productcat", api_version + "/productcat/<string:catid>"],
    ],  # https://maistore.com/productcat
    [
        ProductSubCatList,
        [api_version + "/productsubcats"],
    ],  # https://maistore.com/productsubcats
    [
        ProductSubCat,
        [
            api_version + "/productsubcat",
            api_version + "/productsubcat/<string:subcatid>",
        ],
    ],  # https://maistore.com/productsubcat
    [
        ProductSizeList,
        [api_version + "/productsizes"],
    ],  # https://maistore.com/productsizes
    [
        ProductSize,
        [api_version + "/productsize", api_version + "/productsize/<string:sizeid>"],
    ],  # https://maistore.com/productsizes
    [ColorList, [api_version + "/colors"]],  # https://maistore.com/colors
    [
        Color,
        [api_version + "/color", api_version + "/color/<string:colorid>"],
    ],  # https://maistore.com/color
    [
        ProductColorList,
        [api_version + "/productcolors"],
    ],  # https://maistore.com/productcolors
    [
        ProductColor,
        [api_version + "/productcolor", api_version + "/productcolor/<string:productcolorid>"],
    ],  # https://maistore.com/productcolor
]

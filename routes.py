from resources.productsubcat import ProductSubCatList, ProductSubCat
from resources.user import (
    User,
    UserList,
    UserRegister,
    UserLogin,
    TokenRefresh,
    UserLogout,
    Forgot_Password,
    Change_User_Email,
    Change_User_Password,
    Change_User_Image,
    Change_User_Root_Status,
    Change_User_Admin_Status
)
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.store import Store, StoreList, StorePagenate
from resources.product import Product, ProductList, ProductPagenate
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
        [api_version + "/confirmation/user/<string:email>"],
    ],  # https://mistore.com/confirmation/user/1
    [UserLogin, [api_version + "/login"]],  # https://mistore.com/register
    [UserLogout, [api_version + "/logout"]],  # https://mistore.com/register
    [User, [api_version + "/user/<string:user_id>"]],  # https://mistore.com/user/1
    [UserList, [api_version + "/users"]],  # https://mistore.com/users
    [
        Store,
        [api_version + "/store/<string:store_id>", api_version + "/store"],
    ],  # https://maistore.com/store/1
    [StoreList, [api_version + "/stores"]],  # https://maistore.com/store
    [
        StorePagenate,
        [api_version + "/stores/pagenate/<int:page>"],
    ],  # https://maistore.com/stores/pagenate/1
    [ProductList, [api_version + "/products"]],  # https://maistore.com/product
    [
        ProductPagenate,
        [api_version + "/products/pagenate/<int:page>"],
    ],  # https://maistore.com/products/pagenate/1
    [
        Product,
        [api_version + "/product/<string:product_id>", api_version + "/product"],
    ],  # https://mistore.com/product/bags
    [
        ProductCatList,
        [api_version + "/productcats"],
    ],  # https://maistore.com/productcats
    [
        ProductCat,
        [api_version + "/productcat", api_version + "/productcat/<string:cat_id>"],
    ],  # https://maistore.com/productcat
    [
        ProductSubCatList,
        [api_version + "/productsubcats"],
    ],  # https://maistore.com/productsubcats
    [
        ProductSubCat,
        [
            api_version + "/productsubcat",
            api_version + "/productsubcat/<string:subcat_id>",
        ],
    ],  # https://maistore.com/productsubcat
    [
        ProductSizeList,
        [api_version + "/productsizes"],
    ],  # https://maistore.com/productsizes
    [
        ProductSize,
        [api_version + "/productsize", api_version + "/productsize/<string:size_id>"],
    ],  # https://maistore.com/productsizes
    [ColorList, [api_version + "/colors"]],  # https://maistore.com/colors
    [
        Color,
        [api_version + "/color", api_version + "/color/<string:color_id>"],
    ],  # https://maistore.com/color
    [
        ProductColorList,
        [api_version + "/productcolors"],
    ],  # https://maistore.com/productcolors
    [
        ProductColor,
        [
            api_version + "/productcolor",
            api_version + "/productcolor/<string:productcolor_id>",
        ],
    ],  # https://maistore.com/productcolor
    [
        Change_User_Email,
        [
            api_version + "/change_user_email/<string:user_id>",
        ],
    ],  # https://maistore.com/change_user_email/1
    [
        Change_User_Password,
        [
            api_version + "/change_user_password/<string:user_id>",
        ],
    ],  # https://maistore.com/change_user_password/1
    [
        Change_User_Admin_Status,
        [
            api_version + "/change_user_admin_status/<string:user_id>",
        ],
    ],  # https://maistore.com/change_user_admin_status/1
    [
        Change_User_Root_Status,
        [
            api_version + "/change_user_root_status/<string:user_id>",
        ],
    ],  # https://maistore.com/change_user_root_status/1
    [
        Forgot_Password,
        [
            api_version + "/forgot_password/<string:user_id>",
        ],
    ],  # https://maistore.com/forgot_password/1
    [
        Change_User_Image,
        [
            api_version + "/change_user_image/<string:user_id>",
        ],
    ],  # https://maistore.com/change_user_image/1
]

# i want to comment all the Resources i have created
# work on storelocation
# work on storeemail
# work on storephone
# work on storefav
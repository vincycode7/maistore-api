from resources.productsubcat import ProductSubCatList, ProductSubCat
from resources.user import (
    User,
    UserList,
    UserRegister,
    UserLogin,
    TokenRefresh,
    UserLogout,
    Change_User_Email,
    Change_User_Password,
    Change_User_Image,
    Change_User_Root_Status,
    Change_User_Admin_Status
)
from resources.forgot_password import ( 
                                            RequestForgotPasswordDigit, 
                                            GetForgotPasswordId,
                                            ViewForgotPasswordRequests,
                                            ResetPassword
                                        )
from resources.confirmation import (
                                            ConfirmUser, 
                                            ViewConfirmation, 
                                            RequestConfirmationDigit
                                    )
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
        ConfirmUser,
        [api_version + "/confirm_user/user/<string:email>n"],
    ],  # https://mistore.com/confirm_user/v@gm.com
    [
        ViewConfirmation,
        [api_version + "/view_user_confirmations/user/<string:email>"],
    ],  # https://mistore.com/view_user_confirmations/user/v@gm.com
    [
        RequestConfirmationDigit,
        [api_version + "/request_confirmation_digit"],
    ],  # https://mistore.com/resend_confirmation/user/v@gm.com
    [UserLogin, [api_version + "/login"]],  # https://mistore.com/login
    [UserLogout, [api_version + "/logout"]],  # https://mistore.com/logout
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
    ],  # https://maistore.com/productsize
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
        Change_User_Image,
        [
            api_version + "/change_user_image/<string:user_id>",
        ],
    ],  # https://maistore.com/change_user_image/1
    [
        RequestForgotPasswordDigit,
        [api_version + "/request_forgot_password_digit"],
    ],  # https://mistore.com/request_forgot_password_digit
    [
        GetForgotPasswordId,
        [
            api_version + "/get_forgot_password_id/user/<string:email>",
        ],
    ],  # https://maistore.com/get_forgot_password_id/user/v@gm.com
    [
        ViewForgotPasswordRequests,
        [
            api_version + "/view_forgot_password_requests/user/<string:email>",
        ],
    ],  # https://maistore.com/view_forgot_password_requests/user/v@gm.com
    [
        ResetPassword,
        [
            api_version + "/reset_password/<string:forgotpassword_id>",
        ],
    ],  # https://maistore.com/reset_password/1
]

# i want to comment all the Resources i have created
# work on storelocation
# work on storeemail
# work on storephone
# work on storefav
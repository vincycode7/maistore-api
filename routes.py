from resources.store import Store, StoreList
from resources.user import User, UserList, UserRegister
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

route_path = [
                [UserRegister, ["/register"]], #https://mistore.com/register
                [User, ['/user/<int:userid>']], #https://mistore.com/user/1
                [UserList , ["/users"]], #https://mistore.com/users
                [Store, ["/store/<string:storename>"]], #https://maistore.com/store/shoprite
                [StoreList, ["/stores"]], #https://maistore.com/store
                [ProductList, ["/products"]], #https://mistore.com/product
                [Product, ['/product/<string:productname>']] #https://mistore.com/product/bags
            ]
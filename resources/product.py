import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.product import ProductModel
from error_messages import *
from schemas.product import ProductSchema

schema = ProductSchema()
schema_many = ProductSchema(many=True)

# parser is now a class variable
PARSER = reqparse.RequestParser()
PARSER.add_argument(
    "productname", type=str, required=True, help=BLANK_ERROR.format("productname")
)
PARSER.add_argument(
    "price", type=float, required=True, help=BLANK_ERROR.format("price")
)
PARSER.add_argument(
    "category",
    type=str,
    required=True,
    help=BLANK_ERROR.format("product_category"),
)
PARSER.add_argument(
    "store_id",
    type=str,
    required=True,
    help=BLANK_ERROR.format("store_id"),
)
PARSER.add_argument(
    "quantity",
    type=int,
    default=1,
    required=False,
    help=TO_INPUT.format("quantity"),
)
PARSER.add_argument(
    "is_available",
    type=bool,
    default=False,
    required=False,
    help=TO_INPUT.format("product_availability"),
)

# class to create user and get user
class ProductList(Resource):
    # use for authentication before calling get
    @classmethod
    def get(cls):
        products = ProductModel.find_all()
        if products:
            return {"items": [product.json() for product in products]}, 201
        return {"message": NOT_FOUND.format("products")}, 400


class Product(Resource):

    # use for authentication before calling get
    @classmethod
    def get(cls, productid):

        product = ProductModel.find_by_id(productid=productid)

        if product:
            return {"item": product.json()}, 201
        return {"message": NOT_FOUND.format("product")}, 400

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def post(cls):
        claim = get_jwt_claims()
        data = PARSER.parse_args()
        store = ProductModel.store_queryby_id(store_id=data["store_id"])

        if not store:
            return {"message": NOT_FOUND.format("store")}, 401
        elif not claim["is_admin"] and store.user_id != claim["userid"]:
            return {"message": ADMIN_PRIVILEDGE_REQUIRED}, 401

        product = ProductModel(**data)

        # insert
        try:
            product.save_to_db()
        except Exception as e:
            print(e)
            return {
                "message": ERROR_WHILE_INSERTING.format("product")
            }, 500  # Internal server error
        return product.json(), 201

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def delete(cls, productid, userid=None, password=None):
        product = ProductModel.find_by_id(productid=productid)
        claim = get_jwt_claims()

        if product:
            if (
                not claim["is_admin"]
                and product.json().get("user_id") != claim["userid"]
            ):
                return {"message": ADMIN_PRIVILEDGE_REQUIRED}, 401
            product.delete_from_db()
            return {"message": DELETED.format("product")}, 200  # 200 ok
        elif not claim["is_admin"]:
            return {"message": ADMIN_PRIVILEDGE_REQUIRED}, 401

        return {"message": NOT_FOUND.format("product")}, 401  # 400 is for bad request

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def put(cls, productid):

        data = PARSER.parse_args()

        product = ProductModel.find_by_id(productid=productid)

        if product:
            # update
            for each in data.keys():
                product.__setattr__(each, data[each])
            product.save_to_db()

        else:
            # insert
            product = ProductModel(**data)
            product.save_to_db()

        return product.json(), 201

        # TODO -- EDIT THE JSON FILE FOR STORE, PRODUCT TO RETURN USER_ID AND STORE_ID

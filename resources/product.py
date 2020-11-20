import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.product import *
from schemas.product import ProductSchema

schema = ProductSchema()
put_schema = ProductSchema(exclude=("store_id",))
schema_many = ProductSchema(many=True)

# class to get all product
class ProductList(Resource):
    # use for authentication before calling get
    @classmethod
    # @jwt_optional
    def get(cls, pagenate=False):
        products = ProductModel.find_all()
        if products:
            return {"products": schema_many.dump(products)}, 201

        return {"message": gettext("product_not_found")}, 404


# class to get to get products using pagenate
class ProductPagenate(Resource):
    # use for authentication before calling get
    @classmethod
    # @jwt_optional
    def get(cls, page=1):
        args_ = ProductModel.get_data_()
        products = ProductModel.find_all_pagenate(page=page, **args_)
        items = products.pop("items", None)
        products["products"] = schema_many.dump(items)

        if products.get("products", None):
            return products, 200

        return {"message": gettext("products_not_found")}, 400


class Product(Resource):
    # use for authentication before calling get
    @classmethod
    # @jwt_optional
    def get(cls, product_id):

        product = ProductModel.find_by_id(id=product_id)

        if product:
            return {"product": schema.dump(product)}, 201
        return {"message": gettext("product_not_found")}, 400

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def post(cls):
        claim = get_jwt_claims()
        data = schema.load(ProductModel.get_data_())

        # check if data already exist
        unique_input_error, status = ProductModel.post_unique_already_exist(
            claim=claim, product_data=data
        )
        if unique_input_error:
            return unique_input_error, status

        product = ProductModel(**data)

        # insert
        try:
            product.save_to_db()
        except Exception as e:
            print(f"error is {e}")
            return {
                "message": gettext("product_err_insertion_failed")
            }, 500  # Internal server error
        return schema.dump(product), 201

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def delete(cls, product_id):
        product = ProductModel.find_by_id(id=product_id)
        if not product:
            return {"message": gettext("product_not_found")}, 404

        msg, status_code, _ = ProductModel.auth_by_admin_root_or_user(
            user_id=product.users.id, get_err="product_req_ad_priv_to_delete"
        )
        if status_code != 200:
            return msg, status_code

        try:
            product.delete_from_db()
        except Exception as e:
            print(f"error is {e}")
            return {"message": gettext("Internal_server_error")}, 500
        return {"message": gettext("product_deleted")}, 200  # 200 ok

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def put(cls, product_id):
        data = put_schema.load(ProductModel.get_data_())
        product, unique_input_error, status = ProductModel.put_unique_already_exist(
            product_id=product_id, product_data=data
        )

        if unique_input_error:
            return unique_input_error, status

        if product:
            # update
            for each in data.keys():
                product.__setattr__(each, data[each])

            try:
                product.save_to_db()
                return schema.dump(product), 201
            except Exception as e:
                print(f"error is {e}")
                return {
                    "message": gettext("product_err_insertion_failed")
                }, 500  # Internal server error

        return {"message": gettext("product_not_found")}, 404  # 400 is for bad request

import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.product import ProductModel
from error_messages import *
from schemas.product import ProductSchema

schema = ProductSchema()
schema_many = ProductSchema(many=True)

# class to get all product
class ProductList(Resource):
    # use for authentication before calling get
    @classmethod
    def get(cls, pagenate=False):
        products = ProductModel.find_all()
        if products:
            return {"products": schema_many.dump(products)}, 201

        return {"message": NOT_FOUND.format("products")}, 400


# class to get to get products using pagenate
class ProductPagenate(Resource):
    # use for authentication before calling get
    @classmethod
    def get(cls, page=1):
        args_ = ProductModel.get_data_() 
        products = ProductModel.find_all_pagenate(page=page, **args_)
        items = products.pop("items", None)
        products["products"] = schema_many.dump(items)

        if products.get("products", None):
            return products, 200

        return {"message": NOT_FOUND.format("products")}, 400


class Product(Resource):

    # use for authentication before calling get
    @classmethod
    def get(cls, product_id):

        product = ProductModel.find_by_id(id=product_id)

        if product:
            return {"product": schema.dump(product)}, 201
        return {"message": NOT_FOUND.format("product")}, 400

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
                "message": ERROR_WHILE_INSERTING.format("product")
            }, 500  # Internal server error
        return schema.dump(product), 201

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def delete(cls, product_id):
        product = ProductModel.find_by_id(id=product_id)
        claim = get_jwt_claims()

        if not product:
            return {"message": NOT_FOUND.format("product")}, 401

        if (
            not claim["is_admin"]
            or not claim["is_root"]
            or product.user.id != claim["userid"]
        ):
            return {"message": ADMIN_PRIVILEDGE_REQUIRED.format("delete product")}, 401

        try:
            product.delete_from_db()
        except Exception as e:
            print(f"error is {e}")
            return {"message": INTERNAL_ERROR}, 500
        return {"message": DELETED.format("product")}, 200  # 200 ok

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def put(cls, product_id):
        claim = get_jwt_claims()
        data = schema.load(ProductModel.get_data_())
        product, unique_input_error, status = ProductModel.put_unique_already_exist(
            claim=claim, product_id=product_id, product_data=data
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
                    "message": ERROR_WHILE_INSERTING.format("Product")
                }, 500  # Internal server error

        return {"message": NOT_FOUND.format("Product")}, 400  # 400 is for bad request

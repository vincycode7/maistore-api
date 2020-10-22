import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.product import ProductModel
from error_messages import *
from schemas.product import ProductSchema

schema = ProductSchema()
schema_many = ProductSchema(many=True)

# class to create user and get user
class ProductList(Resource):
    # use for authentication before calling get
    @classmethod
    def get(cls):
        products = ProductModel.find_all()
        if products:
            return {"products": schema_many.dump(products)}, 201
        return {"message": NOT_FOUND.format("products")}, 400


class Product(Resource):

    # use for authentication before calling get
    @classmethod
    def get(cls, productid):

        product = ProductModel.find_by_id(id=productid)

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
        unique_input_error, status = ProductModel.post_unique_already_exist(claim=claim, product_data=data)
        if unique_input_error:
            return unique_input_error, status

        product = ProductModel(**data)

        # insert
        try:
            product.save_to_db()
        except Exception as e:
            print(e)
            return {
                "message": ERROR_WHILE_INSERTING.format("product")
            }, 500  # Internal server error
        return schema.dump(product), 201

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def delete(cls, productid, userid=None, password=None):
        product = ProductModel.find_by_id(id=productid)
        claim = get_jwt_claims()

        if product:
            if (
                not claim["is_admin"]
                and schema.dump(product).get("user_id") != claim["userid"]
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
        claim = get_jwt_claims()
        data = schema.load(ProductModel.get_data_())

        product = ProductModel.find_by_id(id=productid)

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

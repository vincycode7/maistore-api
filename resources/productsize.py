import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.productsize import *
from schemas.productsize import ProductSizeSchema

schema = ProductSizeSchema()
schema_many = ProductSizeSchema(many=True)

# class to list all productsize
class ProductSizeList(Resource):
    @classmethod
    def get(cls):
        productsizes = ProductSizeModel.find_all()
        if productsizes:
            return {"productsizes": schema_many.dump(productsizes)}, 201
        return {"message": gettext("product_size_not_found")}, 404


# class to add product sizes
class ProductSize(Resource):
    def get(self, size_id):
        productsize = ProductSizeModel.find_by_id(id=size_id)
        if productsize:
            return {"productsize": schema.dump(productsize)}, 201
        return {"message": gettext("product_size_not_found")}, 404

    @jwt_required
    def post(self):
        claim = get_jwt_claims()
        data = schema.load(ProductSizeModel.get_data_())

        # check if data already exist
        unique_input_error, status = ProductSizeModel.post_unique_already_exist(
            claim, data
        )
        if unique_input_error:
            return unique_input_error, status

        productsize = ProductSizeModel(**data)

        # save
        try:
            productsize.save_to_db()
        except Exception as e:
            print(f"error is {e}")
            return {
                "message": gettext("Internal_server_error")
            }, 500  # Internal server error
        return schema.dump(productsize), 201

    @jwt_required
    def put(self, size_id):
        claim = get_jwt_claims()
        data = schema.load(ProductSizeModel.get_data_())

        # confirm the unique key to be same with the product route
        (
            productsize,
            unique_input_error,
            status,
        ) = ProductSizeModel.put_unique_already_exist(
            claim=claim, size_id=size_id, size_data=data
        )

        if unique_input_error:
            return unique_input_error, status

        # if user already exist update the dictionary
        if productsize:
            for each in data.keys():
                productsize.__setattr__(each, data[each])
            # save
            try:
                productsize.save_to_db()
                return schema.dump(productsize), 201
            except Exception as e:
                print(f"error is {e}")
                return {
                    "message": gettext("Internal_server_error")
                }, 500  # Internal server error
        return {
            "message": gettext("product_size_not_found")
        }, 404  # 400 is for bad request

    @jwt_required
    def delete(self, size_id):
        msg, status_code, _ = cls.auth_by_admin_root(
            get_err="product_color_req_ad_priv_to_post"
        )
        if status_code != 200:
            return msg, status_code

        productsize = ProductSizeModel.find_by_id(id=size_id)
        if productsize:
            productsize.delete_from_db()
            return {"message": gettext("product_size_deleted")}, 200  # 200 ok
        return {
            "message": gettext("product_size_not_found")
        }, 404  # 400 is for bad request

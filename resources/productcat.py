import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.productcat import *
from schemas.productcat import ProductCatSchema

schema = ProductCatSchema()
schema_many = ProductCatSchema(many=True)
# class to list all productcat
class ProductCatList(Resource):
    @classmethod
    def get(cls):
        productcats = ProductCatModel.find_all()
        if productcats:
            return {"product_categories": schema_many.dump(productcats)}, 201
        return {"message": gettext("product_cat_not_found")}, 404


# class to add product categories
class ProductCat(Resource):
    def get(self, cat_id):
        productcat = ProductCatModel.find_by_id(id=cat_id)
        if productcat:
            return {"product_category": schema.dump(productcat)}, 201
        return {"message": gettext("product_cat_not_found")}, 404

    @jwt_required
    def post(self):
        data = schema.load(ProductCatModel.get_data_())

        # check if data already exist
        unique_input_error, status = ProductCatModel.post_unique_already_exist(data)
        if unique_input_error:
            return unique_input_error, status

        productcat = ProductCatModel(**data)

        # save
        try:
            productcat.save_to_db()
        except Exception as e:
            print(f"error is {e}")
            return {
                "message": gettext("Internal_server_error")
            }, 500  # Internal server error
        return schema.dump(productcat), 201

    @jwt_required
    def put(self, cat_id):
        data = schema.load(ProductCatModel.get_data_())

        # confirm the unique key to be same with the product route
        (
            productcat,
            unique_input_error,
            status,
        ) = ProductCatModel.put_unique_already_exist(cat_id=cat_id, cat_data=data)

        if unique_input_error:
            return unique_input_error, status

        # if user already exist update the dictionary
        if productcat:
            for each in data.keys():
                productcat.__setattr__(each, data[each])

            # save
            try:
                productcat.save_to_db()
                return schema.dump(productcat), 201
            except Exception as e:
                print(f"error is {e}")
                return {
                    "message": gettext("Internal_server_error")
                }, 500  # Internal server error
        return {
            "message": gettext("product_cat_not_found")
        }, 404  # 400 is for bad request

    @jwt_required
    def delete(self, cat_id):
        msg, status_code, _ = ProductCatModel.auth_by_admin_root(
            get_err="product_cat_req_ad_priv_to_delete"
        )
        if status_code != 200:
            return msg, status_code
        productcat = ProductCatModel.find_by_id(id=cat_id)
        if productcat:
            productcat.delete_from_db()
            return {"message": gettext("product_cat_deleted")}, 200  # 200 ok
        return {
            "message": gettext("product_cat_not_found")
        }, 400  # 400 is for bad request

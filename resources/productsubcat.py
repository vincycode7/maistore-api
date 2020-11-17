import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.productsubcat import *
from schemas.productsubcat import ProductSubCatSchema

schema = ProductSubCatSchema()
schema_many = ProductSubCatSchema(many=True)
# class to list all productsubcat
class ProductSubCatList(Resource):
    @classmethod
    def get(cls):
        productsubcats = ProductSubCatModel.find_all()
        if productsubcats:
            return {"product_subcategorys": schema_many.dump(productsubcats)}, 201
        return {"message": gettext("product_subcat_not_found")}, 404


# class to add product subcategories
class ProductSubCat(Resource):
    def get(self, subcat_id):
        productsubcat = ProductSubCatModel.find_by_id(id=subcat_id)
        if productsubcat:
            return {"product_subcategory": schema.dump(productsubcat)}, 201
        return {"message": gettext("product_subcat_not_found")}, 404

    @jwt_required
    def post(self):
        data = schema.load(ProductSubCatModel.get_data_())

        # check if data already exist
        unique_input_error, status = ProductSubCatModel.post_unique_already_exist(data)
        if unique_input_error:
            return unique_input_error, status

        productsubcat = ProductSubCatModel(**data)

        # save
        try:
            productsubcat.save_to_db()
        except Exception as e:
            print(f"error is {e}")
            return {
                "message": gettext("Internal_server_error")
            }, 500  # Internal server error
        return schema.dump(productsubcat), 201

    @jwt_required
    def put(self, subcat_id):
        data = schema.load(ProductSubCatModel.get_data_())

        # confirm the unique key to be same with the product route
        (
            productsubcat,
            unique_input_error,
            status,
        ) = ProductSubCatModel.put_unique_already_exist(
            subcat_id=subcat_id, subcat_data=data
        )

        if unique_input_error:
            return unique_input_error, status

        # if product_subcategory already exist update the dictionary
        if productsubcat:
            for each in data.keys():
                productsubcat.__setattr__(each, data[each])

            # save
            try:
                productsubcat.save_to_db()
                return schema.dump(productsubcat), 201
            except Exception as e:
                print(f"error is {e}")
                return {
                    "message": gettext("Internal_server_error")
                }, 500  # Internal server error
        return {"message": gettext("product_subcat_not_found")}, 404

    @jwt_required
    def delete(self, subcat_id):
        # check subcat permission, edit and parse data
        msg, status_code, _ = cls.auth_by_admin_root(
            get_err="product_subcat_req_ad_priv_to_delete"
        )
        if status_code != 200:
            return None, msg, status_code

        productsubcat = ProductSubCatModel.find_by_id(id=subcat_id)
        if productsubcat:
            productsubcat.delete_from_db()
            return {"message": DELETED.format("Product subcategory")}, 200  # 200 ok
        return {
            "message": gettext("product_subcat_not_found")
        }, 404  # 400 is for bad request

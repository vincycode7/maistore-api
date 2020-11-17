import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.productcol import *
from schemas.productcol import ProductColorSchema

schema = ProductColorSchema()
schema_many = ProductColorSchema(many=True)


# class to list all ProductColors
class ProductColorList(Resource):
    @classmethod
    def get(cls):
        productcolors = ProductColorModel.find_all()
        if productcolors:
            return {"productcolors": schema_many.dump(productcolors)}, 201
        return {"message": gettext("prduct_color_rel_exist_not_found")}, 404


# class to add product colors
class ProductColor(Resource):
    def get(self, productcolor_id):
        productcolor = ProductColorModel.find_by_id(id=productcolor_id)
        if productcolor:
            return {"productcolor": schema.dump(productcolor)}, 201
        return {"message": gettext("prduct_color_rel_exist_not_found")}, 404

    @jwt_required
    def post(self):
        data = schema.load(ProductColorModel.get_data_())

        # check if data already exist
        unique_input_error, status = ProductColorModel.post_unique_already_exist(data)
        if unique_input_error:
            return unique_input_error, status

        productcolor = ProductColorModel(**data)

        # save
        try:
            productcolor.save_to_db()
        except Exception as e:
            print(f"error is {e}")
            return {
                "message": gettext("Internal_server_error")
            }, 500  # Internal server error
        return schema.dump(productcolor), 201

    @jwt_required
    def put(self, productcolor_id):
        data = schema.load(ProductColorModel.get_data_())

        # confirm the unique key to be same with the product route
        (
            productcolor,
            unique_input_error,
            status,
        ) = ProductColorModel.put_unique_already_exist(
            productcolor_id=productcolor_id, productcol_data=data
        )

        if unique_input_error:
            return unique_input_error, status

        # if user already exist update the dictionary
        if productcolor:
            for each in data.keys():
                productcolor.__setattr__(each, data[each])
            # save
            try:
                productcolor.save_to_db()
                return schema.dump(productcolor), 201
            except Exception as e:
                print(f"error is {e}")
                return {
                    "message": gettext("Internal_server_error")
                }, 500  # Internal server error
        return {
            "message": gettext("prduct_color_rel_not_found")
        }, 404  # 400 is for bad request

    @jwt_required
    def delete(self, productcolor_id):
        productcolor = ProductColorModel.find_by_id(id=productcolor_id)
        if not productcolor:
            return {"message": gettext("prduct_color_rel_not_found")}, 404

        msg, status_code, _ = ProductColorModel.auth_by_admin_root_or_user(
            user_id=product.store.user_id, get_err="product_color_req_ad_priv_to_delete"
        )
        if status_code != 200:
            return msg, status_code

        try:
            productcolor.delete_from_db()
        except Exception as e:
            print(f"error is {e}")
            return {"message": gettext("Internal_server_error")}, 500
        return {"message": gettext("product_color_rel_deleted")}, 200  # 200 ok

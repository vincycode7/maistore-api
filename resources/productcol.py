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
    @jwt_required
    def get(cls):
        productcolors = ProductColorModel.find_all()
        if productcolors:
            return {"productcolors": schema_many.dump(productcolors)}, 201
        return {"message": NOT_FOUND.format("productcolors")}, 400


# class to add product colors
class ProductColor(Resource):
    @jwt_required
    def get(self, productcolorid):
        productcolor = ProductColorModel.find_by_id(id=productcolorid)
        if productcolor:
            return {"productcolor": schema.dump(productcolor)}, 201
        return {"message": NOT_FOUND.format("productcolor")}, 400

    @jwt_required
    def post(self):
        claim = get_jwt_claims()
        data = schema.load(ProductColorModel.get_data_())

        # check if data already exist
        unique_input_error, status = ProductColorModel.post_unique_already_exist(
            claim, data
        )
        if unique_input_error:
            return unique_input_error, status

        productcolor = ProductColorModel(**data)

        # save
        try:
            productcolor.save_to_db()
        except Exception as e:
            print(f"error is {e}")
            return {
                "message": ERROR_WHILE_INSERTING.format("product color")
            }, 500  # Internal server error
        return schema.dump(productcolor), 201

    @jwt_required
    def put(self, productcolorid):
        claim = get_jwt_claims()
        data = schema.load(ProductColorModel.get_data_())

        # confirm the unique key to be same with the product route
        (
            productcolor,
            unique_input_error,
            status,
        ) = ProductColorModel.put_unique_already_exist(
            claim=claim, productcolorid=productcolorid, productcol_data=data
        )

        if unique_input_error:
            return unique_input_error, status

        # if user already exist update the dictionary
        if productcolor:
            for each in data.keys():
                productcolor.__setattr__(each, data[each])
            # else:
            #     # check if data already exist
            #     unique_input_error, status = ProductColorModel.post_unique_already_exist(claim, data)
            #     if unique_input_error:
            #         return unique_input_error, status
            #     productcolor = ProductColorModel(**data)

            # save
            try:
                productcolor.save_to_db()
                return schema.dump(productcolor), 201
            except Exception as e:
                print(f"error is {e}")
                return {
                    "message": ERROR_WHILE_INSERTING.format("product color")
                }, 500  # Internal server error
        return {
            "message": NOT_FOUND.format("product color")
        }, 400  # 400 is for bad request

    @jwt_required
    def delete(self, productcolorid):
        claim = get_jwt_claims()
        productcolor = ProductColorModel.find_by_id(id=productcolorid)
        if not productcolor:
            return {"message": NOT_FOUND.format("product color")}, 401

        if (
            not claim["is_admin"] or not claim["is_root"]
            or productcolor.product.store.user.id != claim["userid"]
            ):
            return {
                "message": ADMIN_PRIVILEDGE_REQUIRED.format("delete product color")
            }, 401

        try:
            productcolor.delete_from_db()
        except Exception as e:
            print(e)
            return {"message": INTERNAL_ERROR}, 500
        return {"message": DELETED.format("product color")}, 200  # 200 ok
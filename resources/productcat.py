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
        return {"message": NOT_FOUND.format("productcats")}, 400


# class to add product categories
class ProductCat(Resource):
    def get(self, cat_id):
        productcat = ProductCatModel.find_by_id(id=cat_id)
        if productcat:
            return {"product_category": schema.dump(productcat)}, 201
        return {"message": NOT_FOUND.format("productcats")}, 400

    @jwt_required
    def post(self):
        claim = get_jwt_claims()
        data = schema.load(ProductCatModel.get_data_())

        # check if data already exist
        unique_input_error, status = ProductCatModel.post_unique_already_exist(
            claim, data
        )
        if unique_input_error:
            return unique_input_error, status

        productcat = ProductCatModel(**data)

        # save
        try:
            productcat.save_to_db()
        except Exception as e:
            print(f"error is {e}")
            return {
                "message": ERROR_WHILE_INSERTING.format("product category")
            }, 500  # Internal server error
        return schema.dump(productcat), 201

    @jwt_required
    def put(self, cat_id):
        claim = get_jwt_claims()
        data = schema.load(ProductCatModel.get_data_())

        # confirm the unique key to be same with the product route
        (
            productcat,
            unique_input_error,
            status,
        ) = ProductCatModel.put_unique_already_exist(
            claim=claim, cat_id=cat_id, cat_data=data
        )

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
                    "message": ERROR_WHILE_INSERTING.format("product category")
                }, 500  # Internal server error
        return {
            "message": NOT_FOUND.format("Product category")
        }, 400  # 400 is for bad request

    @jwt_required
    def delete(self, cat_id):
        claim = get_jwt_claims()
        if not claim["is_admin"] or not claim["is_root"]:
            return {
                "message": ADMIN_PRIVILEDGE_REQUIRED.format("delete product category")
            }, 401
        productcat = ProductCatModel.find_by_id(id=cat_id)
        if productcat:
            productcat.delete_from_db()
            return {"message": DELETED.format("Product category")}, 200  # 200 ok
        return {
            "message": NOT_FOUND.format("Product category")
        }, 400  # 400 is for bad request

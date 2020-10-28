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
    @jwt_required
    def get(cls):
        productsubcats = ProductSubCatModel.find_all()
        if productsubcats:
            return {"product_subcategorys": schema_many.dump(productsubcats)}, 201
        return {"message": NOT_FOUND.format("productsubcats")}, 400


# class to add product subcategories
class ProductSubCat(Resource):
    @jwt_required
    def get(self, subcat_id):
        productsubcat = ProductSubCatModel.find_by_id(id=subcat_id)
        if productsubcat:
            return {"product_subcategory": schema.dump(productsubcat)}, 201
        return {"message": NOT_FOUND.format("productsubcats")}, 400

    @jwt_required
    def post(self):
        claim = get_jwt_claims()
        data = schema.load(ProductSubCatModel.get_data_())

        # check if data already exist
        unique_input_error, status = ProductSubCatModel.post_unique_already_exist(
            claim, data
        )
        if unique_input_error:
            return unique_input_error, status

        productsubcat = ProductSubCatModel(**data)

        # save
        try:
            productsubcat.save_to_db()
        except Exception as e:
            print(f"error is {e}")
            return {
                "message": ERROR_WHILE_INSERTING.format("product subcategory")
            }, 500  # Internal server error
        return schema.dump(productsubcat), 201

    @jwt_required
    def put(self, subcat_id):
        claim = get_jwt_claims()
        data = schema.load(ProductSubCatModel.get_data_())

        # confirm the unique key to be same with the product route
        (
            productsubcat,
            unique_input_error,
            status,
        ) = ProductSubCatModel.put_unique_already_exist(
            claim=claim, subcat_id=subcat_id, subcat_data=data
        )

        if unique_input_error:
            return unique_input_error, status

        # if product_subcategory already exist update the dictionary
        if productsubcat:
            for each in data.keys():
                productsubcat.__setattr__(each, data[each])
            # else:
            #     # check if data already exist
            #     unique_input_error, status = ProductSubCatModel.post_unique_already_exist(claim, data)
            #     if unique_input_error:
            #         return unique_input_error, status
            #     productsubcat = ProductSubCatModel(**data)

            # save
            try:
                productsubcat.save_to_db()
                return schema.dump(productsubcat), 201
            except Exception as e:
                print(f"error is {e}")
                return {
                    "message": ERROR_WHILE_INSERTING.format("product subcategory")
                }, 500  # Internal server error
        return {
            "message": NOT_FOUND.format("Product subcategory")
        }, 400  # 400 is for bad request

    @jwt_required
    def delete(self, subcat_id):
        claim = get_jwt_claims()
        if not claim["is_admin"] or not claim["is_root"]:
            return {
                "message": ADMIN_PRIVILEDGE_REQUIRED.format(
                    "delete product subcategory"
                )
            }, 401
        productsubcat = ProductSubCatModel.find_by_id(id=subcat_id)
        if productsubcat:
            productsubcat.delete_from_db()
            return {"message": DELETED.format("Product subcategory")}, 200  # 200 ok
        return {
            "message": NOT_FOUND.format("Product subcategory")
        }, 400  # 400 is for bad request

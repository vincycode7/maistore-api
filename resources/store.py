from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_claims, fresh_jwt_required
from models.store import StoreModel
from error_messages import *
from schemas.store import StoreSchema

reg_schema = StoreSchema()
reg_schema_many = StoreSchema(many=True)

class Store(Resource):
    @classmethod
    @jwt_required
    def get(cls, storeid):
        store = StoreModel.find_by_id(storeid)
        if store:
            return reg_schema.dump(store)
        else:
            return {"message": NOT_FOUND.format("store")}, 404

    @classmethod
    @jwt_required
    def post(cls):
        claim = get_jwt_claims()
        data_or_err,status = parser_or_err(reg_schema,request.get_json())
        if status == 400: return data_or_err

        if not claim["is_admin"] and claim["userid"] != data_or_err["user_id"]:
            return {"message": ADMIN_PRIVILEDGE_REQUIRED}, 401

        if StoreModel.find_by_name(storename=data_or_err["storename"]):
            return {"message": ALREADY_EXISTS.format("store", data_or_err["storename"])}, 400

        store = StoreModel(**data_or_err)
        try:
            store.save_to_db()
        except Exception as e:
            print(e)
            return {"message": ERROR_WHILE_INSERTING.format("store.")}, 500

        return reg_schema.dump(store), 201

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def put(cls, storeid):
        claim = get_jwt_claims()
        data_or_err,status = parser_or_err(reg_schema,request.get_json())
        if status == 400: return data_or_err

        if not claim["is_admin"] and claim["userid"] != data_or_err["user_id"]:
            return {"message": ADMIN_PRIVILEDGE_REQUIRED}, 401

        store_byid = StoreModel.find_by_id(storeid=storeid)
        store_byname = StoreModel.find_by_name(storename=data_or_err["storename"])

        # check if store name is in use
        if store_byid:
            if store_byname:
                if store_byname.storename != store_byid.storename:
                    return {
                        "message": ALREADY_EXISTS.format(
                            "store", store_byname.storename
                        )
                    }, 400  # 400 is for bad request

            # update
            try:
                for each in data_or_err.keys():
                    store_byid.__setattr__(each, data_or_err[each])
                store_byid.save_to_db()
            except Exception as e:
                print(f"error is {e} dd")
                return {
                    "message": ERROR_WHILE_INSERTING.format("item")
                }, 500  # Internal server error
        else:
            if store_byname:
                return {
                    "message": ALREADY_EXISTS.format("store", store_byname.storename)
                }, 400  # 400 is for bad request
            try:
                # confirm the unique key to be same with the product route
                store_byid = StoreModel(**data_or_err)
                store_byid.save_to_db()
            except Exception as e:
                print(f"error is {e}")
                return {
                    "message": ERROR_WHILE_INSERTING.format("item")
                }, 500  # Internal server error

        return reg_schema.dump(store_byid), 201

    @classmethod
    @fresh_jwt_required
    def delete(cls, storeid):
        claim = get_jwt_claims()
        store = StoreModel.find_by_id(storeid)

        if store:
            if not claim["is_admin"] and claim["userid"] != store.user_id:
                return {"message": ADMIN_PRIVILEDGE_REQUIRED}, 401
            store.delete_from_db()
            return {"message": DELETED.format("Store")}
        elif not store and not claim["is_admin"]:
            return {"message": ADMIN_PRIVILEDGE_REQUIRED}, 401
        return {"message": NOT_FOUND.format("Store")}


class StoreList(Resource):
    @classmethod
    def get(cls):
        stores = StoreModel.find_all()
        return {"stores": reg_schema_many.dump(stores)}

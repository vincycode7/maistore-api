from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_claims, fresh_jwt_required
from models.store import StoreModel
from error_messages import *
from schemas.store import StoreSchema

schema = StoreSchema()
schema_many = StoreSchema(many=True)


class Store(Resource):
    @classmethod
    @jwt_required
    def get(cls, storeid):
        store = StoreModel.find_by_id(storeid)
        if store:
            return schema.dump(store)
        else:
            return {"message": NOT_FOUND.format("store")}, 404

    @classmethod
    @jwt_required
    def post(cls):
        claim = get_jwt_claims()
        data = schema.load(StoreModel.get_data_())

        # check if data already exist
        unique_input_error, status = StoreModel.post_unique_already_exist(claim, data)
        if unique_input_error:
            return unique_input_error, status

        store = StoreModel(**data)
        try:
            store.save_to_db()
        except Exception as e:
            print(e)
            return {"message": ERROR_WHILE_INSERTING.format("store.")}, 500

        return schema.dump(store), 201

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def put(cls, storeid):
        claim = get_jwt_claims()
        data = schema.load(StoreModel.get_data_())
        store, unique_input_error, status = StoreModel.put_unique_already_exist(
            claim=claim, storeid=storeid, store_data=data
        )
        if unique_input_error:
            return unique_input_error, status

        print(f"store --> {store}, {store.id}")
        if store:
            for each in data.keys():
                store.__setattr__(each, data[each])  # update
            # else:
            #     store = StoreModel(**data)

            try:
                print("after this")
                store.save_to_db()
                print("didnt get here")
                return schema.dump(store), 201
            except Exception as e:
                print(f"error is {e}")
                return {
                    "message": ERROR_WHILE_INSERTING.format("store")
                }, 500  # Internal server error
        return {"message": NOT_FOUND.format("store id")}, 400  # 400 is for bad request

    @classmethod
    @fresh_jwt_required
    def delete(cls, storeid):
        claim = get_jwt_claims()
        store, unique_input_error, status = StoreModel.delete_auth(
            claim=claim, storeid=storeid
        )
        if unique_input_error:
            return unique_input_error, status

        try:
            store.delete_from_db()
        except Exception as e:
            print(e)
            return {"message": INTERNAL_ERROR}, 500
        return {"message": DELETED.format("Store")}


class StoreList(Resource):
    @classmethod
    def get(cls):
        stores = StoreModel.find_all()
        if stores:
            return {"stores": schema_many.dump(stores)}, 201

        return {"message": NOT_FOUND.format("stores")}, 400

# class to get to get stores using pagenate
class StorePagenate(Resource):
    # use for authentication before calling get
    @classmethod
    def get(cls, page=1):
        args_ = StoreModel.get_data_() 
        stores = StoreModel.find_all_pagenate(page=page, **args_)
        items = stores.pop("items", None)
        stores["stores"] = schema_many.dump(items)

        if stores.get("stores", None):
            return stores, 200

        return {"message": NOT_FOUND.format("stores")}, 400

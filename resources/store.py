from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, fresh_jwt_required
from models.store import StoreModel
from error_messages import *


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        name="storename",
        required=True,
        help=BLANK_ERROR.format("storename"),
        type=str,
        case_sensitive=False,
    )
    parser.add_argument(
        name="user_id",
        required=True,
        help=BLANK_ERROR.format("user_id"),
        type=int,
        case_sensitive=False,
    )
    parser.add_argument(
        name="country",
        required=False,
        help="Country where the store is located",
        type=str,
        case_sensitive=False,
    )

    @classmethod
    @jwt_required
    def get(cls, storeid):
        store = StoreModel.find_by_id(storeid)
        if store:
            return store.json()
        else:
            return {"message": NOT_FOUND.format("store")}, 404

    @classmethod
    @jwt_required
    def post(cls):
        claim = get_jwt_claims()
        data = Store.parser.parse_args()
        if not claim["is_admin"] and claim["userid"] != data["user_id"]:
            return {"message": ADMIN_PRIVILEDGE_REQUIRED}, 401

        if StoreModel.find_by_name(storename=data["storename"]):
            return {"message": ALREADY_EXISTS.format("store", data["storename"])}, 400

        store = StoreModel(**data)
        try:
            store.save_to_db()
        except Exception as e:
            print(e)
            return {"message": ERROR_WHILE_INSERTING.format("store.")}, 500

        return store.json(), 201

    # use for authentication before calling post
    @classmethod
    @jwt_required
    def put(cls, storeid):
        claim = get_jwt_claims()
        data = Store.parser.parse_args()

        if not claim["is_admin"] and claim["userid"] != data["user_id"]:
            return {"message": ADMIN_PRIVILEDGE_REQUIRED}, 401

        store_byid = StoreModel.find_by_id(storeid=storeid)
        store_byname = StoreModel.find_by_name(storename=data["storename"])

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
                for each in data.keys():
                    store_byid.__setattr__(each, data[each])
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
                store_byid = StoreModel(**data)
                store_byid.save_to_db()
            except Exception as e:
                print(f"error is {e}")
                return {
                    "message": ERROR_WHILE_INSERTING.format("item")
                }, 500  # Internal server error

        return store_byid.json(), 201

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
        return {"stores": [store.json() for store in stores]}

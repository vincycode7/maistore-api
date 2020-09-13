from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(name="storename", required=True, help="a store name is required to proceed", type=str,case_sensitive=False)
    parser.add_argument(name="user_id", required=True, help="only active users can create a store", type=str,case_sensitive=False)
    parser.add_argument(name="location", required=False, help="a store location is good for business",case_sensitive=False)

    def get(self, storename):
        store = StoreModel.find_by_name(storename=storename)
        if store:
            return store.json()
        else:
            return {"message" : "store not found"}, 404

    def post(self, storename):
        storename = storename.lower()
        if StoreModel.find_by_name(storename=storename):
            return {"message" : f"A store with name {storename} already exists"}, 400

        data = Store.parser.parse_args()
        message = StoreModel.check_form_integrity(storename=storename, data=data)
        if message: return message

        store = StoreModel(**data)
        try:
            store.save_to_db()
        except Exception as e:
            print(e)
            return {"message" : "An error occured while creating the store."}, 500

        return store.json(), 201

    def delete(self, storename):
        store = StoreModel.find_by_name(storename=storename)

        if store:
            store.delete_from_db()

        return {"message" : "Store deleted"}


class StoreList(Resource):
    def get(self):
        stores = StoreModel.findall()
        if stores:
            return {"stores" : [store.json() for store in stores]}
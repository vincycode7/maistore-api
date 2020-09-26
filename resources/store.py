from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(name="storename", required=True, help="a store name is required to proceed", type=str,case_sensitive=False)
    parser.add_argument(name="user_id", required=True, help="only active users can create a store", type=str,case_sensitive=False)
    parser.add_argument(name="country", required=False, help="Country where the store is located", type=str,case_sensitive=False)

    def get(self, storeid):
        store = StoreModel.find_by_id(storeid)
        if store:
            return store.json()
        else:
            return {"message" : "store not found"}, 404

    def post(self):
        data = Store.parser.parse_args()

        if StoreModel.find_by_name(storename=data["storename"]):
            return {"message" : f"A store with name {data['storename']} already exists"}, 400

        store = StoreModel(**data)
        try:
            store.save_to_db()
        except Exception as e:
            print(e)
            return {"message" : "An error occured while creating the store."}, 500

        return store.json(), 201

    #use for authentication before calling post
    def put(self, storeid):
        data = Store.parser.parse_args()
        store_byid = StoreModel.find_by_id(storeid=storeid)
        store_byname = StoreModel.find_by_name(storename=data["storename"])

        #check if store name is in use
        if store_byid:
            if store_byname:
                if store_byname.storename!= store_byid.storename: return {"message" : f"store name {store_byname.storename} already exists."},400 # 400 is for bad request
        
            #update
            try:
                for each in data.keys(): store_byid.__setattr__(each, data[each])
                store_byid.save_to_db()                
            except Exception as e:
                print(f"error is {e} dd")
                return {"message" : "An error occured updating the item the item"}, 500 #Internal server error
        else:
            if store_byname: return {"message" : f"store name {store_byname.storename} already in use."},400 # 400 is for bad request
            try:
                    #confirm the unique key to be same with the product route
                    store_byid = StoreModel(**data)
                    store_byid.save_to_db()
            except Exception as e:
                print(f"error is {e} -- yy")
                return {"message" : "An error occured creating the item"}, 500 #Internal server error
    
        return store_byid.json(), 201

    def delete(self, storeid):
        store = StoreModel.find_by_id(storeid)

        if store:
            store.delete_from_db()
            return {"message" : "Store deleted"}

        return {"message" : "Store not found"}


class StoreList(Resource):
    def get(self):
        stores = StoreModel.find_all()
        print(f"all all {stores}")
        return {"stores" : [store.json() for store in stores]}
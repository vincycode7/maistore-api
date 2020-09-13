import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.product import ProductModels

#class to create user and get user
class ProductList(Resource):
    @jwt_required() #use for authentication before calling get
    def get(self):

        products = ProductModels.find_all()
        if products: return {"items" : [ product.json() for product in products]},201
        return {"message" : 'Items not found'}, 400


class Product(Resource):

    #parser is now a class variable
    parser = reqparse.RequestParser()
    parser.add_argument('productname', type=str, required=True, help="productname field is required")
    parser.add_argument('price', type=float, required=True, help="price field is requried")
    parser.add_argument('quantity', type=int, required=True, help="quantity field is required")
    parser.add_argument("category", type=str, required=True, help="category the product falls in is required")
    parser.add_argument("store_id", type=str, required=True, help="store_id of the user posting the product is required")

    @jwt_required() #use for authentication before calling get
    def get(self, productname):

        product = ProductModels.find_by_name(productname=productname)

        if product: return {"item" : product.json()},201
        return {"message" : 'Item not found'}, 400

    @jwt_required() #use for authentication before calling post
    def post(self, productname):
        data = Product.parser.parse_args()

        #check form integrety
        message = ProductModels.check_form_integrity(productname, data)

        if message:
            return message
        
        product = ProductModels.instance_from_dict(dict_=data)

        #insert
        try:
            print(f"{product}")
            product.save_to_db()
        except Exception as e:
            print(e)
            return {"message" : "An error occured inserting the item"}, 500 #Internal server error

        return product.json(), 201

    @jwt_required() #use for authentication before calling post
    def delete(self, productname, username=None, password=None):
        product = ProductModels.find_by_name(productname=productname)
        if product:
            product.delete_from_db()
            return {"message" : "Item deleted"}, 200 # 200 ok
            
        return {"message" : "Item Not in database"}, 401 # 400 is for bad request


    @jwt_required() #use for authentication before calling post
    def put(self, productname):
        
        data = Product.parser.parse_args()
        message = ProductModels.check_form_integrity(productname, data)

        if message: return message

        product = ProductModels.find_by_name(productname=data["productname"])

        if product:
            #update
            for each in data.keys(): product.__setattr__(each, data[each])
            product.save_to_db()

        else:
            #insert
            product = ProductModels.instance_from_dict(dict_=data)
            product.save_to_db()

        return product.json(), 201

        
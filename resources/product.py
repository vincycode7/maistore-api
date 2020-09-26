import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.product import ProductModel

#class to create user and get user
class ProductList(Resource):
    #use for authentication before calling get
    def get(self):
        products = ProductModel.find_all()
        if products: return {"items" : [ product.json() for product in products]},201
        return {"message" : 'Items not found'}, 400


class Product(Resource):

    #parser is now a class variable
    parser = reqparse.RequestParser()
    parser.add_argument('productname', type=str, required=True, help="productname field is required")
    parser.add_argument('price', type=float, required=True, help="price field is requried")
    parser.add_argument("category", type=str, required=True, help="category the product falls in is required")
    parser.add_argument("store_id", type=str, required=True, help="store_id of the user posting the product is required")
    parser.add_argument('quantity', type=int, default=1, required=False, help="quantity field is required")
    parser.add_argument("is_available", type=bool, default=False, required=False, help="1 if propuct is available and 0 if not available")

    #use for authentication before calling get
    def get(self, productid):

        product = ProductModel.find_by_id(productid=productid)

        if product: return {"item" : product.json()},201
        return {"message" : 'Item not found'}, 400

    #use for authentication before calling post
    def post(self):
        data = Product.parser.parse_args()
        
        product = ProductModel(**data)

        #insert
        try:
            product.save_to_db()
        except Exception as e:
            print(e)
            return {"message" : "An error occured inserting the item"}, 500 #Internal server error
        return product.json(), 201

    #use for authentication before calling post
    def delete(self, productid, userid=None, password=None):
        product = ProductModel.find_by_id(productid=productid)
        if product:
            product.delete_from_db()
            return {"message" : "Item deleted"}, 200 # 200 ok
            
        return {"message" : "Item Not in database"}, 401 # 400 is for bad request


    #use for authentication before calling post
    def put(self, productid):
        
        data = Product.parser.parse_args()

        product = ProductModel.find_by_id(productid=productid)

        if product:
            #update
            for each in data.keys(): product.__setattr__(each, data[each])
            product.save_to_db()

        else:
            #insert
            product = ProductModel(**data)
            product.save_to_db()

        return product.json(), 201
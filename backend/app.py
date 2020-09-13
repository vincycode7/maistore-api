from resources.user import User, UserList, UserRegister
from resources.product import Product, ProductList
from resources.store import Store, StoreList
from flask import Flask, request
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from flask_restful import Resource, Api, reqparse

"""

    Flask is the main framework for the project
    flask_jwt is used for authentication via tokens
    flask_restful makes working with flask alot easier
    Flask SQLAlchemy is used to easily store data to a relational database
"""

#export PATH="$PATH:/home/vcode/.local/bin"
#runner : reset && python app.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app=app)
app.secret_key = "vcode" #always remember to get the apps's secret key, also this key should be hidden from the public.

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) #creates a new end point called */auth*

class PaymentList(Resource):
    def get(self):
        return [], 200 #return the product

class Payment(Resource):
    def get(self, paymentid):
        return {'payment' : paymentid} #returns the list of payments

    def post(self, paymentid):
        data = request.get_json(silent=True)
        if data == None: return {"message" : "Invalid object type, use json."}, 404
        

#User
api.add_resource(UserRegister, "/register") #https://mistore.com/register
api.add_resource(User, '/user/<string:username>') #https://mistore.com/gbenga
# api.add_resource(Users, '/user/<string:name>?<string:password>') #https://mistore.com/gbenga
api.add_resource(UserList , "/users") #https://mistore.com//student

#store
api.add_resource(Store, "/store/<string:storename>") #https://maistore.com/store/shoprite
api.add_resource(StoreList, "/stores") #https://maistore.com/store

#product
api.add_resource(ProductList, "/products") #https://mistore.com/product
api.add_resource(Product, '/product/<string:productname>') #https://mistore.com/product/bags


#payment
# api.add_resource(Payment, '/payment/<string:paymentid>') #https://mistore.com/payment/h47j32U89
# api.add_resource(PaymentList, "/payment") #https://mistore.com/product

if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
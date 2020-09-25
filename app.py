import os
from flask import Flask, request
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from flask_restful import Resource, Api, reqparse
from routes import *

"""

    Flask is the main framework for the project
    flask_jwt is used for authentication via tokens
    flask_restful makes working with flask alot easier
    Flask SQLAlchemy is used to easily store data to a relational database
"""

#export PATH="$PATH:/home/vcode/.local/bin"
#runner : reset && python app.py

def create_app(secret_key):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.secret_key = secret_key #always remember to get the apps's secret key, also this key should be hidden from the public.
    
    return app

def create_api(app):
    api = Api(app=app)
    return api
    
def create_jwt(app, auth, identity):
    jwt = JWT(app, auth, identity) #creates a new end point called */auth*
    return jwt

def link_route_path(api):
    for route, path in route_path: api.add_resource(route, path)
    return api

# create app
app = create_app(secret_key="vcode")
api = create_api(app)
jwt = create_jwt(app, authenticate, identity)
link_route_path(api=api)

if __name__ == "__main__":
    from db import db

    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    app.run(port=5000, debug=True)
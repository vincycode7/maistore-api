import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from app_setup import *
from init_models import *
from routes import *

"""

    Flask is the main framework for the project
    flask_jwt is used for authentication via tokens
    flask_restful makes working with flask alot easier
    Flask SQLAlchemy is used to easily store data to a relational database
"""

# export PATH="$PATH:/home/vcode/.local/bin"
# runner : reset && python app.py
# create app
# set up config for app, jwt and api
app = Flask(__name__)
app, cors, jwt, api = create_and_config_app(app=app, route_path=route_path)

if __name__ == "__main__":

    @app.before_first_request
    def create_tables():
        db.create_all()
        create_usr_from_root(app=app)


    app.run(port=7001, debug=True)

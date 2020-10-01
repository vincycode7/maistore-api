import os
from flask import Flask, request, jsonify
from marshmallow import ValidationError
from app_config import *
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
app, jwt, api = create_and_config_app(app=app, route_path=route_path)
if __name__ == "__main__":
    from db import db
    from ma import ma

    @app.before_first_request
    def create_tables():
        db.create_all()

    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        return jsonify(err.message), 400

    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)

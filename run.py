from app import app, create_usr_from_root
from db import db
from ma import ma

@app.before_first_request
def create_tables():
    db.create_all()
    create_usr_from_root(app=app)

db.init_app(app)
ma.init_app(app)

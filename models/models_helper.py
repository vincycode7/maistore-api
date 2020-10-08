from db import db
from typing import List, Dict
from error_messages import *
from datetime import datetime as dt
from blacklist import BLACKLIST_ACCESS
from flask import request, json
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_optional,
    get_jwt_claims,
    get_jwt_identity,
    jwt_refresh_token_required,
    get_current_user,
    get_raw_jwt,
    get_csrf_token,
    decode_token,
)


class ModelsHelper:
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self):
        # connect to the database
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        result = cls.query.all()
        return result

    @classmethod
    def find_by_id(cls, id):
        result = cls.query.filter_by(id=id).first()
        return result

    @staticmethod
    def get_data_():
        """ 
            function to get data from user, if first approach fails
            tries the second.
        """
        data = dict(request.values)
        print(f"first --> {data} \n second --> {request.get_data(as_text=True)}")
        if data: 
            return data
        data = request.get_data(as_text=True)
        if not data:
            return None
        return json.loads(request.get_data(as_text=True))
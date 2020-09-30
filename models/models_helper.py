from db import db
from typing import List, Dict
from error_messages import *
from datetime import datetime as dt

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
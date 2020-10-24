import traceback
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

    def rollback_error(self):
        db.session.rollback()

    @classmethod
    def find_all(cls):
        result = cls.query.all()
        return result

    @classmethod
    def find_all(cls):
        result = cls.query.all()
        return result

    @classmethod
    def find_all_pagenate(
                            cls,
                            page=None, 
                            per_page=None, 
                            error_out=True, 
                            max_per_page=None
                        ):
        result = cls.query.pagenate(
                                    page=page, 
                                    per_page=per_page, 
                                    error_out=error_out, 
                                    max_per_page=max_per_page
                                )
        return result

    @classmethod
    def find_by_productid_and_colorid(cls, productid=None, colorid=None):
        from models.productcol import ProductColorModel
        result = ProductColorModel.query.filter_by(
                                                    productid=productid, 
                                                    colorid=colorid
                                                ).first()
        return result

    @classmethod
    def find_by_prodcatid_prodsubcatid_desc(cls, productcatid=None, productsubcatid=None, desc=None):
        from models.productsize import ProductSizeModel
        result = ProductSizeModel.query.filter_by(
                                                    productcatid=productcatid, 
                                                    productsubcatid=productsubcatid, 
                                                    desc=desc
                                                ).first()
        return result

    @classmethod
    def find_user_by_id(cls, userid):
        from models.user import UserModel
        return UserModel.find_by_id(id=userid)

    @classmethod
    def find_productcat_by_id(cls, productcatid):
        from models.productcat import ProductCatModel
        return ProductCatModel.find_by_id(id=productcatid)
    
    @classmethod
    def find_productsubcat_by_id(cls, productsubcatid):
        from models.productsubcat import ProductSubCatModel
        return ProductSubCatModel.find_by_id(id=productsubcatid)

    @classmethod
    def find_store_by_id(cls, storeid):
        from models.store import StoreModel
        return StoreModel.find_by_id(id=storeid)

    @classmethod
    def find_size_by_id(cls, sizeid):
        from models.productsize import ProductSizeModel
        return ProductSizeModel.find_by_id(id=sizeid)
    
    @classmethod
    def find_product_by_id(cls, productid):
        from models.product import ProductModel
        return ProductModel.find_by_id(id=productid)

    @classmethod
    def find_color_by_id(cls, colorid):
        from models.colors import ColorsModel
        return ColorsModel.find_by_id(id=colorid)

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

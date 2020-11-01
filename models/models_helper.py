import traceback
from db import db
from typing import List, Dict
from error_messages import *
from datetime import datetime as dt
from blacklist import BLACKLIST_ACCESS
from flask import request, json
from marshmallow import INCLUDE, EXCLUDE
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
    def rollback_error(cls):
        db.session.rollback()

    @classmethod
    def find_all(cls):
        result = cls.query.all()
        return result

    @classmethod
    def find_all_pagenate(
        cls,
        page=1,
        per_page=10,
        error_out=True,
        max_per_page=None,
        left_edge=2,
        left_current=3,
        right_current=3,
        right_edge=2,
    ):

        # /page=None, per_page=None, error_out=True,max_per_page=None,left_edge=2, left_current=2, right_current=5, right_edge=2"
        result = cls.query.paginate(
            page=int(page), per_page=int(per_page), error_out=int(error_out), max_per_page=max_per_page
        )
        result = {
            "has_next": result.has_next,
            "has_prev": result.has_prev,
            "items": result.items,
            "iter_pages": list(
                result.iter_pages(
                    left_edge=int(left_edge),
                    left_current=int(left_current),
                    right_current=int(right_current),
                    right_edge=int(right_edge),
                )
            ),
            "page" : result.page,
            "pages" : result.pages,
            "per_page" : result.per_page,
            "prev_num" : result.prev_num,
            "total" : result.total
        }
        return result

    @classmethod
    def find_by_productid_and_colorid(cls, product_id=None, color_id=None):
        from models.productcol import ProductColorModel

        result = ProductColorModel.query.filter_by(
            product_id=product_id, color_id=color_id
        ).first()
        return result

    @classmethod
    def find_by_prodcatid_prodsubcatid_desc(
        cls, productcat_id=None, productsubcat_id=None, desc=None
    ):
        from models.productsize import ProductSizeModel

        result = ProductSizeModel.query.filter_by(
            productcat_id=productcat_id, productsubcat_id=productsubcat_id, desc=desc
        ).first()
        return result

    @classmethod
    def find_user_by_id(cls, user_id):
        from models.user import UserModel
        return UserModel.find_by_id(id=user_id)

    @classmethod
    def find_user_by_email(cls, user_email):
        from models.user import UserModel
        return UserModel.find_by_email(email=user_email)

    @classmethod
    def find_productcat_by_id(cls, productcat_id):
        from models.productcat import ProductCatModel

        return ProductCatModel.find_by_id(id=productcat_id)

    @classmethod
    def find_productsubcat_by_id(cls, productsubcat_id):
        from models.productsubcat import ProductSubCatModel

        return ProductSubCatModel.find_by_id(id=productsubcat_id)

    @classmethod
    def find_store_by_id(cls, store_id):
        from models.store import StoreModel

        return StoreModel.find_by_id(id=store_id)

    @classmethod
    def find_size_by_id(cls, size_id):
        from models.productsize import ProductSizeModel

        return ProductSizeModel.find_by_id(id=size_id)

    @classmethod
    def find_product_by_id(cls, product_id):
        from models.product import ProductModel

        return ProductModel.find_by_id(id=product_id)

    @classmethod
    def find_color_by_id(cls, color_id):
        from models.colors import ColorsModel

        return ColorsModel.find_by_id(id=color_id)

    @classmethod
    def find_by_id(cls, id):
        result = cls.query.filter_by(id=id).first()
        return result

    @staticmethod
    def auth_by_admin_root_or_user(user_id, err_msg):
        claim = get_jwt_claims()
        print(claim["userid"] , user_id)
        if not claim["is_admin"] and not claim["is_root"] and claim["userid"] != user_id:
            return {
                "message": ADMIN_PRIVILEDGE_REQUIRED.format(err_msg)
            }, 401, claim
        return False, 200, claim

    @staticmethod
    def auth_by_admin_root(err_msg):
        claim = get_jwt_claims()
        if not claim["is_admin"] and not claim["is_root"]:
            return {
                "message": ADMIN_PRIVILEDGE_REQUIRED.format(err_msg)
            }, 401, claim
        return False, 200, claim

    @staticmethod
    def auth_by_root(err_msg):
        claim = get_jwt_claims()
        if  not claim["is_root"]:
            return {
                "message": ROOT_PRIVILEDGE_REQUIRED.format(err_msg)
            }, 401, claim
        return False, 200, claim
    
    @staticmethod
    def auth_by_admin(err_msg):
        claim = get_jwt_claims()
        if not claim["is_admin"]:
            return {
                "message": ADMIN_PRIVILEDGE_REQUIRED.format(err_msg)
            }, 401, claim
        return False, 200, claim

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
            return {}
        return json.loads(request.get_data(as_text=True))

import traceback
from db import db
from typing import List, Dict
from datetime import datetime as dt
from blacklist import BLACKLIST_ACCESS
from flask import request, json
from marshmallow import INCLUDE, EXCLUDE, ValidationError
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
from libs.mailer import MailerException
from libs.strings import TranslatorException, gettext, change_locale

class ModelHelperException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class UserException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ConfirmationException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ColorException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ForgotPasswordException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ProductException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ProductCatException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ProductSizeException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ProductSubCatException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class StoreException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ModelsHelper:
    def delete_from_db(self, get_err="Internal_server_error"):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            try:
                raise ModelHelperException(gettext(get_err).format(e))
            except:
                raise ModelHelperException(gettext(get_err))

    def save_to_db(self, get_err="Internal_server_error"):
        # connect to the database
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            try:
                raise ModelHelperException(gettext(get_err).format(e))
            except:
                raise ModelHelperException(gettext(get_err))

    @classmethod
    def rollback_error(cls, get_err="Internal_server_error"):
        try:
            db.session.rollback()
        except Exception as e:
            try:
                raise ModelHelperException(gettext(get_err).format(e))
            except:
                raise ModelHelperException(gettext(get_err))

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
            page=int(page),
            per_page=int(per_page),
            error_out=int(error_out),
            max_per_page=max_per_page,
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
            "page": result.page,
            "pages": result.pages,
            "per_page": result.per_page,
            "prev_num": result.prev_num,
            "total": result.total,
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
        from models.users import UserModel

        return UserModel.find_by_id(id=user_id)

    @classmethod
    def find_user_by_email(cls, user_email):
        from models.users import UserModel

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
    def auth_by_admin_root_or_user(user_id, get_err):
        try:
            claim = get_jwt_claims()
            if (
                not claim["is_admin"]
                and not claim["is_root"]root_usr
                and claim["userid"] != user_id
            ):
                return {"message": gettext(get_err)}, 401, claim
        except Exception as e:
            raise ModelHelperException(
                gettext("model_helper_err_chk_ad_priv").format(e)
            )
        except:
            raise ModelHelperException(gettext("model_helper_err_chk_ad_priv"))
        return False, 200, claim

    @staticmethod
    def auth_by_admin_root(get_err):
        try:
            claim = get_jwt_claims()
            if not claim["is_admin"] and not claim["is_root"]:
                return {"message": gettext(get_err)}, 401, claim
        except Exception as e:
            raise ModelHelperException(
                gettext("model_helper_err_chk_ad_priv").format(e)
            )
        except:
            raise ModelHelperException(gettext("model_helper_err_chk_ad_priv"))
        return False, 200, claim

    @staticmethod
    def auth_by_root(get_err):
        try:
            claim = get_jwt_claims()
            if not claim["is_root"]:
                return {"message": gettext(get_err)}, 401, claim
        except Exception as e:
            raise ModelHelperException(
                gettext("model_helper_err_chk_ad_priv").format(e)
            )
        except:
            raise ModelHelperException(gettext("model_helper_err_chk_ad_priv"))
        return False, 200, claim

    @staticmethod
    def auth_by_admin(get_err):
        try:
            claim = get_jwt_claims()
            if not claim["is_admin"]:
                return {"message": gettext(get_err)}, 401, claim
        except Exception as e:
            raise ModelHelperException(
                gettext("model_helper_err_chk_ad_priv").format(e)
            )
        except:
            raise ModelHelperException(gettext("model_helper_err_chk_ad_priv"))
        return False, 200, claim

    @staticmethod
    def get_data_(get_err="modelhelper_err_getting_value_frm_request"):
        """
        function to get data from user, if first approach fails
        tries the second.
        """
        try:
            data = dict(request.values)
        except Exception as e:
            try:
                raise ModelHelperException(gettext(get_err).format(e))
            except:
                raise ModelHelperException(gettext(get_err))

        if data:
            return data

        try:
            data = request.get_data(as_text=True)
        except Exception as e:
            try:
                raise ModelHelperException(gettext(get_err).format(e))
            except:
                raise ModelHelperException(gettext(get_err))

        if not data:
            return {}

        try:
            return json.loads(request.get_data(as_text=True))
        except Exception as e:
            try:
                raise ModelHelperException(
                    gettext("modelhelper_err_loading_request_value_to_json").format(e)
                )
            except:
                raise ModelHelperException(
                    gettext("modelhelper_err_loading_request_value_to_json")
                )

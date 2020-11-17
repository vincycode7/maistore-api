from models.models_helper import *
from uuid import uuid4

# helper functions
def create_id(context):
    return "PRODUCT-V1-" + uuid4().hex


# helper functions
def is_avail(context):
    quantity = context.current_parameters.get("quantity", 0)
    if quantity > 0:
        return True
    else:
        return False


class ProductModel(db.Model, ModelsHelper):
    __tablename__ = "product"

    id = db.Column(
        db.String(50), primary_key=True, unique=True, default=create_id, nullable=False
    )
    productname = db.Column(db.String(40), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    discount = db.Column(db.Float(precision=2), nullable=False, default=0)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    store_id = db.Column(
        db.String(50),
        db.ForeignKey("store.id"),
        index=False,
        unique=False,
        nullable=False,
    )
    productcat_id = db.Column(
        db.Integer,
        db.ForeignKey("productcat.id"),
        index=False,
        unique=False,
        nullable=False,
    )
    productsubcat_id = db.Column(
        db.Integer,
        db.ForeignKey("productsubcat.id"),
        index=False,
        unique=False,
        nullable=False,
        default=None,
    )
    size_id = db.Column(
        db.Integer,
        db.ForeignKey("productsize.id"),
        index=False,
        unique=False,
        nullable=False,
        default=None,
    )
    used = db.Column(
        db.Boolean,
        index=False,
        unique=False,
        nullable=False,
        default=True,
    )
    is_available = db.Column(
        db.Boolean,
        index=False,
        unique=False,
        nullable=False,
        default=is_avail,
        onupdate=is_avail,
    )

    # merge
    reviews = db.relationship(
        "ReviewModel", lazy="dynamic", backref="product", cascade="all, delete-orphan"
    )

    productcol = db.relationship(
        "ProductColorModel",
        lazy="dynamic",
        backref="product",
        cascade="all, delete-orphan",
    )

    @classmethod
    def find_by_name(cls, productname=None):
        try:
            result = cls.query.filter_by(productname=productname).first()
        except Exception as e:
            raise ProductException(gettext("product_err_get_by_name").format(e))
        except:
            raise ProductException(gettext("product_err_get_by_name"))
        return result

    @classmethod
    def check_unique_inputs(cls, product_data):
        store = cls.find_store_by_id(store_id=product_data.get("store_id", None))
        productcat = cls.find_productcat_by_id(
            productcat_id=product_data.get("productcat_id", None)
        )
        productsubcat = cls.find_productsubcat_by_id(
            productsubcat_id=product_data.get("productsubcat_id", None)
        )
        size = cls.find_size_by_id(size_id=product_data.get("size_id", None))
        return store, productcat, productsubcat, size

    @classmethod
    def post_unique_already_exist(cls, claim, product_data):
        store, productcat, productsubcat, size = cls.check_unique_inputs(
            product_data=product_data
        )

        # check if store exist
        if not store:
            return {"message": gettext("store_not_found")}, 404

        # check if user is admin or normal user
        msg, status_code, _ = cls.auth_by_admin_root_or_user(
            user_id=store.user_id, get_err="color_req_ad_priv_to_edit"
        )
        if status_code != 200:
            return None, msg, status_code

        # check productcat_id
        # check if productcat exist
        if not productcat:
            return {"message": gettext("product_cat_not_found")}, 404

        # check product subcat id
        # check if productsubcat insert exist
        if not productsubcat:
            return {"message": gettext("product_subcat_not_found")}, 404

        # check if size is valid
        # check if size exist
        if not size:
            return {"message": gettext("product_subcat_size_not_found")}, 404

        # check if productsubcat is in product cat
        if productsubcat.productcat.id != productcat.id:
            return {"message": gettext("product_subcat_not_found_in_cat")}, 404

        # check if store id is for current user
        return False, 200

    @classmethod
    def put_unique_already_exist(cls, product_id, product_data):
        # check user permission, edit and parse data
        product = cls.find_by_id(id=product_id)
        store, productcat, productsubcat, size = cls.check_unique_inputs(
            product_data=product_data
        )

        if not product:
            return {"message": gettext("product_not_found")}, 404

        msg, status_code, _ = ProductModel.auth_by_admin_root_or_user(
            user_id=product.store.user_id, get_err="product_req_ad_priv_to_edit"
        )
        if status_code != 200:
            return msg, status_code

        # check if product exist
        if not product:
            return None, {"message": gettext("product_not_found")}, 404

        # check if store exist
        if not store:
            return None, {"message": gettext("store_not_found")}, 404

        # # check if product is in store
        # if product.store.id != store.id:
        #     return (
        #         None,
        #         {
        #             "message": NOT_EQUAL.format(
        #                 "product store id -- " + str(product.store.id),
        #                 "store_id -- " + str(store.id),
        #             )
        #         },
        #         401,
        #     )

        # check productcat_id
        # check if productcat exist
        if not productcat:
            return None, {"message": gettext("productcat_not_found")}, 404

        # check product subcat id
        # check if productsubcat insert exist
        if not productsubcat:
            return None, {"message": gettext("product_subcat_not_found")}, 404

        # check if size is valid
        # check if size exist
        if not size:
            return None, {"message": gettext("product_subcat_size_not_found")}, 404

        # check if productsubcat is in product cat
        if productsubcat.productcat.id != productcat.id:
            return (
                None,
                {"message": gettext("product_subcat_not_found_in_cat")},
                404,
            )

        return product, False, 200

    @classmethod
    def delete_auth(cls, claim, store_id):
        store = StoreModel.find_by_id(store_id)

        if not store:
            return product, {"message": gettext("store_not_found")}, 404

        # if not claim["is_admin"] and claim["userid"] != store.user_id:
        #     return product, {"message": gettext("product_req_ad_priv_to_delete")}, 404
        return product, False, 200


# TODO: Do pagenate in response, for product (i think it's checked).
# TODO: check if i did put request side of product (i think it's checked)
# TODO: check if i did delete auth side of product (i think it's checked)

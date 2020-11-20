from models.models_helper import *


class ProductCatModel(db.Model, ModelsHelper):
    __tablename__ = "productcat"

    # columns
    id = db.Column(db.Integer, primary_key=True, unique=True)
    desc = db.Column(db.String(256), unique=True, nullable=False)

    # merge
    products = db.relationship(
        "ProductModel",
        lazy="dynamic",
        backref="productcat",
        cascade="all, delete-orphan",
    )
    productsubcat = db.relationship(
        "ProductSubCatModel",
        lazy="dynamic",
        backref="productcat",
        cascade="all, delete-orphan",
    )

    productsize = db.relationship(
        "ProductSizeModel",
        lazy="dynamic",
        backref="productcat",
        cascade="all, delete-orphan",
    )

    @classmethod
    def find_by_catdesc(cls, catdesc=None):
        try:
            result = cls.query.filter_by(desc=catdesc).first()
        except Exception as e:
            raise ProductCatException(
                gettext("product_cat_err_getby_catdesc").format(e)
            )
        except:
            raise ProductCatException(gettext("product_cat_err_getby_catdesc"))
        return result

    @classmethod
    def check_unique_inputs(cls, cat_data=None):
        desc = cls.find_by_catdesc(catdesc=cat_data.get("desc", None))
        return desc

    @classmethod
    def post_unique_already_exist(cls, cat_data):
        msg, status_code, _ = cls.auth_by_admin_root(
            get_err="product_cat_req_ad_priv_to_post"
        )
        if status_code != 200:
            return msg, status_code
        desc = cls.check_unique_inputs(cat_data=cat_data)
        if desc:
            return {
                "message": gettext("product_cat_exit")
            }, 400  # 400 is for bad request
        return False, 200

    @classmethod
    def put_unique_already_exist(cls, cat_id, cat_data):
        # check cat permission, edit and parse data
        msg, status_code, _ = cls.auth_by_admin_root(
            get_err="product_cat_req_ad_priv_to_put"
        )
        if status_code != 200:
            return msg, status_code

        productcat = cls.find_by_id(id=cat_id)
        desc = cls.check_unique_inputs(cat_data=cat_data)

        if desc and productcat and desc.id != productcat.id:
            return (
                productcat,
                {"message": gettext("product_cat_exit")},
                400,
            )  # 400 is for bad request
        return productcat, False, 200

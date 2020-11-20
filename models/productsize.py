from models.models_helper import *


class ProductSizeModel(db.Model, ModelsHelper):
    __tablename__ = "productsize"

    # class variables
    id = db.Column(db.Integer, primary_key=True, unique=True)
    productcat_id = db.Column(
        db.Integer, db.ForeignKey("productcat.id"), nullable=False
    )
    productsubcat_id = db.Column(
        db.Integer, db.ForeignKey("productsubcat.id"), nullable=False
    )
    desc = db.Column(db.String(256), nullable=False)

    # merge
    # products = db.relationship(
    #     "ProductModel",
    #     lazy="dynamic",
    #     backref="productsize",
    #     cascade="all, delete-orphan",
    # )

    @classmethod
    def find_by_sizedesc(
        cls, sizedesc=None, get_err="product_size_err_find_by_sizedesc"
    ):
        try:
            result = cls.query.filter_by(desc=sizedesc).first()
        except Exception as e:
            raise ProductSizeException(gettext(get_err).format(e))
        except:
            raise ProductSizeException(gettext(get_err))
        return result

    @classmethod
    def check_unique_inputs(cls, size_data=None):
        prodcat_subcat_desc = cls.find_by_prodcatid_prodsubcatid_desc(
            size_data.get("productcat_id", None),
            size_data.get("productsubcat_id", None),
            size_data.get("desc", None),
        )
        productcat = cls.find_productcat_by_id(
            productcat_id=size_data.get("productcat_id", None)
        )
        productsubcat = cls.find_productsubcat_by_id(
            productsubcat_id=size_data.get("productsubcat_id", None)
        )
        return prodcat_subcat_desc, productcat, productsubcat

    @classmethod
    def post_unique_already_exist(cls, claim, size_data):
        # check if admin
        msg, status_code, _ = cls.auth_by_admin_root(
            get_err="product_color_req_ad_priv_to_post"
        )
        if status_code != 200:
            return msg, status_code

        productsize, productcat, productsubcat = cls.check_unique_inputs(
            size_data=size_data
        )
        # check if the post exist already
        if productsize:
            return {
                "message": gettext("product_size_exist")
            }, 400  # 400 is for bad request

        # check if productcatid exist
        if not productcat:
            return {"message": gettext("product_cat_not_found")}, 404

        # check if productid exist
        if not productsubcat:
            return {"message": gettext("product_subcat_not_found")}, 404

        # check if productid exist
        if not productsubcat.productcat:
            return {"message": gettext("product_cat_for_subcat_not_found")}, 404

        # (before we got here that means we are sure productcat
        # and productsubcat exist) check if productsubcat is
        # not in productcat
        if productsubcat.productcat.id != productcat.id:
            return {"message": gettext("product_cat_for_subcat_not_found")}, 404

        return False, 200

    @classmethod
    def put_unique_already_exist(cls, claim, size_id, size_data):
        # check if admin
        msg, status_code, _ = cls.auth_by_admin_root(
            get_err="product_color_req_ad_priv_to_post"
        )
        if status_code != 200:
            return msg, status_code

        # chcek if record to edit exist
        productsize_record = cls.find_by_id(id=size_id)
        if not productsize_record:
            return (
                None,
                {"message": gettext("product_size_not_found")},
                404,
            )

        # check if the put exist already
        productsize, productcat, productsubcat = cls.check_unique_inputs(
            size_data=size_data
        )
        if productsize and productsize.id != productsize_record.id:
            return (
                None,
                {"message": gettext("product_size_exist")},
                400,
            )  # 400 is for bad request

        # check if productcatid exist
        if not productcat:
            return (
                None,
                {"message": gettext("product_cat_not_found")},
                404,
            )

        # check if productid exist
        if not productsubcat:
            return (
                None,
                {"message": gettext("product_subcat_not_found")},
                404,
            )

        # (before we got here that means we are sure productcat
        # and productsubcat exist) check if productsubcat is
        # not in productcat
        if productsubcat.productcat.id != productcat.id:
            return (
                None,
                {"message": gettext("product_cat_for_subcat_not_found")},
                400,
            )  # 400 is for bad request
        return productsize_record, False, 200


# TODO: make sure to check all options of error when posting or puting

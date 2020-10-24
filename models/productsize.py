from models.models_helper import *


class ProductSizeModel(db.Model, ModelsHelper):
    __tablename__ = "productsize"

    # class variables
    id = db.Column(db.Integer, primary_key=True, unique=True)
    productcatid = db.Column(db.Integer, db.ForeignKey("productcat.id"), nullable=False)
    productsubcatid = db.Column(
        db.Integer, db.ForeignKey("productsubcat.id"), nullable=False
    )
    desc = db.Column(db.String(256), nullable=False)

    # merge
    products = db.relationship(
        "ProductModel",
        lazy="dynamic",
        backref="productsize",
        cascade="all, delete-orphan",
    )

    @classmethod
    def find_by_sizedesc(cls, sizedesc=None):
        result = cls.query.filter_by(desc=sizedesc).first()
        return result

    @classmethod
    def check_unique_inputs(cls, size_data=None):
        prodcat_subcat_desc = cls.find_by_prodcatid_prodsubcatid_desc(
            size_data.get("productcatid", None),
            size_data.get("productsubcatid", None),
            size_data.get("desc", None),
        )
        productcat = cls.find_productcat_by_id(
            productcatid=size_data.get("productcatid", None)
        )
        productsubcat = cls.find_productsubcat_by_id(
            productsubcatid=size_data.get("productsubcatid", None)
        )
        return prodcat_subcat_desc, productcat, productsubcat

    @classmethod
    def post_unique_already_exist(cls, claim, size_data):
        # check if admin
        if not claim or (claim and (not claim["is_admin"] or not claim["is_root"])):
            return {
                "message": ADMIN_PRIVILEDGE_REQUIRED.format("post product sizes")
            }, 401
        productsize, productcat, productsubcat = cls.check_unique_inputs(
            size_data=size_data
        )
        # check if the post exist already
        if productsize:
            return {
                "message": ALREADY_EXISTS.format("product size", size_data["desc"])
            }, 400  # 400 is for bad request

        # check if productcatid exist
        if not productcat:
            return {
                "message": DOES_NOT_EXIST.format(
                    "product category" + " " + str(size_data["productcatid"])
                )
            }, 400  # 400 is for bad request

        # check if productid exist
        if not productsubcat:
            return {
                "message": DOES_NOT_EXIST.format(
                    "product sub category" + " " + str(size_data["productsubcatid"])
                )
            }, 400  # 400 is for bad request

        # (before we got here that means we are sure productcat
        # and productsubcat exist) check if productsubcat is
        # not in productcat
        if productsubcat.productcat.id != productcat.id:
            return {
                "message": NOT_FOUND_IN.format(
                    "product sub category",
                    "category id " + str(size_data["productsubcatid"]),
                )
            }, 400  # 400 is for bad request

        return False, 200

    @classmethod
    def put_unique_already_exist(cls, claim, sizeid, size_data):
        # check if admin
        if not claim or (claim and (not claim["is_admin"] or not claim["is_root"])):
            return (
                None,
                {"message": ADMIN_PRIVILEDGE_REQUIRED.format("post product sizes")},
                401,
            )

        # chcek if record to edit exist
        productsize_record = cls.find_by_id(id=sizeid)
        if not productsize_record:
            return (
                None,
                {"message": NOT_FOUND.format("productsize record")},
                400,
            )  # 400 is for bad request

        # check if the put exist already
        productsize, productcat, productsubcat = cls.check_unique_inputs(
            size_data=size_data
        )
        if productsize and productsize.id != productsize_record.id:
            return (
                None,
                {"message": ALREADY_EXISTS.format("product size", size_data["desc"])},
                400,
            )  # 400 is for bad request

        # check if productcatid exist
        if not productcat:
            return (
                None,
                {
                    "message": DOES_NOT_EXIST.format(
                        "product category" + " " + str(size_data["productcatid"])
                    )
                },
                400,
            )  # 400 is for bad request

        # check if productid exist
        if not productsubcat:
            return (
                None,
                {
                    "message": DOES_NOT_EXIST.format(
                        "product sub category" + " " + str(size_data["productsubcatid"])
                    )
                },
                400,
            )  # 400 is for bad request

        # (before we got here that means we are sure productcat
        # and productsubcat exist) check if productsubcat is
        # not in productcat
        if productsubcat.productcat.id != productcat.id:
            return (
                None,
                {
                    "message": NOT_FOUND_IN.format(
                        "product sub category",
                        "category id " + str(size_data["productsubcatid"]),
                    )
                },
                400,
            )  # 400 is for bad request
        return productsize_record, False, 200


# TODO: make sure to check all options of error when posting or puting

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
        result = cls.query.filter_by(desc=catdesc).first()
        return result

    @classmethod
    def check_unique_inputs(cls, cat_data=None):
        desc = cls.find_by_catdesc(catdesc=cat_data.get("desc", None))
        return desc

    @classmethod
    def post_unique_already_exist(cls, claim, cat_data):
        desc = cls.check_unique_inputs(cat_data=cat_data)
        if desc:
            return {
                "message": ALREADY_EXISTS.format("product category", cat_data["desc"])
            }, 400  # 400 is for bad request
        elif not claim or (claim and (not claim["is_admin"] or not claim["is_root"])):
            return {
                "message": ADMIN_PRIVILEDGE_REQUIRED.format("post product categories")
            }, 401
        return False, 200

    @classmethod
    def put_unique_already_exist(cls, claim, cat_id, cat_data):
        productcat = cls.find_by_id(id=cat_id)
        desc = cls.check_unique_inputs(cat_data=cat_data)

        # check cat permission, edit and parse data
        if not claim or not claim["is_admin"]:
            return (
                productcat,
                {"message": ADMIN_PRIVILEDGE_REQUIRED.format("edit product category")},
                401,
            )
        if desc and productcat and desc.id != productcat.id:
            return (
                productcat,
                {
                    "message": ALREADY_EXISTS.format(
                        "product category", cat_data["desc"]
                    )
                },
                400,
            )  # 400 is for bad request
        return productcat, False, 200

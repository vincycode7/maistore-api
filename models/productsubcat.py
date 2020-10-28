from models.models_helper import *


class ProductSubCatModel(db.Model, ModelsHelper):
    __tablename__ = "productsubcat"

    # columns
    id = db.Column(db.Integer, primary_key=True, unique=True)
    # gatta change this to productcatid
    category_id = db.Column(
        db.Integer, db.ForeignKey("productcat.id"), nullable=False
    )
    desc = db.Column(db.String(256), unique=True, nullable=False)

    # merge
    products = db.relationship(
        "ProductModel",
        lazy="dynamic",
        backref="productsubcat",
        cascade="all, delete-orphan",
    )

    productsize = db.relationship(
        "ProductSizeModel",
        lazy="dynamic",
        backref="productsubcat",
        cascade="all, delete-orphan",
    )

    @classmethod
    def find_by_subcatdesc(cls, subcatdesc=None):
        result = cls.query.filter_by(desc=subcatdesc).first()
        return result

    @classmethod
    def check_unique_inputs(cls, subcat_data=None):
        desc = cls.find_by_subcatdesc(subcatdesc=subcat_data.get("desc", None))
        productcat = cls.find_productcat_by_id(productcat_id=subcat_data.get("category_id", None))
        return desc, productcat

    @classmethod
    def post_unique_already_exist(cls, claim, subcat_data):
        desc, productcat = cls.check_unique_inputs(subcat_data=subcat_data)
        
        if not claim or (claim and (not claim["is_admin"] or not claim["is_root"])):
            return {
                "message": ADMIN_PRIVILEDGE_REQUIRED.format(
                    "post product subcategories"
                )
            }, 401

        if desc:
            return {
                "message": ALREADY_EXISTS.format(
                    "product subcategory", subcat_data["desc"]
                )
            }, 400  # 400 is for bad request

        # check if productid exist
        if not productcat:
            return {
                "message": DOES_NOT_EXIST.format(
                    "product category"
                )
            }, 400  # 400 is for bad request
        return False, 200

    @classmethod
    def put_unique_already_exist(cls, claim, subcat_id, subcat_data):
        productsubcat = cls.find_by_id(id=subcat_id)
        desc = cls.check_unique_inputs(subcat_data=subcat_data)

        # check subcat permission, edit and parse data
        if not claim or (claim and (not claim["is_admin"] or not claim["is_root"])):
            return {
                "message": ADMIN_PRIVILEDGE_REQUIRED.format(
                    "post product subcategories"
                )
            }, 401

        # check if productid exist
        if not productcat:
            return {
                "message": DOES_NOT_EXIST.format(
                    "product category"
                )
            }, 400  # 400 is for bad request

        if desc and productsubcat and desc.id != productsubcat.id:
            return (
                productsubcat,
                {
                    "message": ALREADY_EXISTS.format(
                        "product subcategory", subcat_data["desc"]
                    )
                },
                400,
            )  # 400 is for bad request
        return productsubcat, False, 200

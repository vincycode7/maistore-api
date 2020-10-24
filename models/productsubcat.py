from models.models_helper import *


class ProductSubCatModel(db.Model, ModelsHelper):
    __tablename__ = "productsubcat"

    # columns
    id = db.Column(db.Integer, primary_key=True, unique=True)
    # gatta change this to productcatid
    categorycatid = db.Column(
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
        return desc

    @classmethod
    def post_unique_already_exist(cls, claim, subcat_data):
        desc = cls.check_unique_inputs(subcat_data=subcat_data)
        if desc:
            return {
                "message": ALREADY_EXISTS.format(
                    "product subcategory", subcat_data["desc"]
                )
            }, 400  # 400 is for bad request
        elif not claim or (claim and (not claim["is_admin"] or not claim["is_root"])):
            return {
                "message": ADMIN_PRIVILEDGE_REQUIRED.format(
                    "post product subcategories"
                )
            }, 401
        return False, 200

    @classmethod
    def put_unique_already_exist(cls, claim, subcatid, subcat_data):
        productsubcat = cls.find_by_id(id=subcatid)
        desc = cls.check_unique_inputs(subcat_data=subcat_data)

        # check subcat permission, edit and parse data
        if not claim or not claim["is_admin"]:
            return (
                productsubcat,
                {
                    "message": ADMIN_PRIVILEDGE_REQUIRED.format(
                        "edit product subcategory"
                    )
                },
                401,
            )
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
        # elif productsubcat and desc and claim["is_admin"]:
        #     return (
        #         productsubcat,
        #         {"message" : NOTHING_TO_UPDATE},
        #         400,
        #     )  # 400 is for bad request
        return productsubcat, False, 200

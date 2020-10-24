from models.models_helper import *
from uuid import uuid4

# helper functions
def create_id(context):
    return "PRODUCT-V1-" + uuid4().hex


# helper functions
def is_avail(context):
    quantity = context.get_current_parameters().get("quantity", 0)
    if quantity > 0:
        print(f"quantity --> {quantity}")
        return True
    else:
        print(f"quantity --> {quantity}")
        return False


class ProductModel(db.Model, ModelsHelper):
    __tablename__ = "product"

    id = db.Column(
        db.String(50), primary_key=True, unique=True, default=create_id, nullable=False
    )
    productname = db.Column(db.String(40), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False, default=0)
    discount = db.Column(db.Float(precision=2), nullable=False, default=0)
    quantity = db.Column(db.Integer, nullable=False, default=0)
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
        nullable=True,
        default=None,
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
        result = cls.query.filter_by(productname=productname).first()
        return result

    @classmethod
    def check_unique_inputs(cls, product_data):
        store = cls.find_store_by_id(storeid=product_data.get("store_id", None))
        productcat = cls.find_productcat_by_id(productcatid=product_data.get("productcat_id", None))
        productsubcat = cls.find_productsubcat_by_id(productsubcatid=product_data.get("productsubcat_id", None))
        size = cls.find_size_by_id(sizeid=product_data.get("size_id", None))
        return store, productcat, productsubcat, size

    @classmethod
    def post_unique_already_exist(cls, claim, product_data):
        store, productcat, productsubcat, size = cls.check_unique_inputs(product_data=product_data)

        # check if store exist
        if not store:
            return {"message": NOT_FOUND.format("store")}, 401

        # check if user is admin or normal user
        if not claim["is_admin"] or not claim["is_root"]  or claim["userid"] != store.user.id:
            return {"message": ADMIN_PRIVILEDGE_REQUIRED.format("to post a store")}, 401

        # check productcatid
        # check if productcat exist
        if not productcat:
            return {"message": NOT_FOUND.format("productcat")}, 401

        # check product subcat id
        # check if productsubcat insert exist
        if not productsubcat:
            return {"message": NOT_FOUND.format("productsubcat")}, 401

        #check if size is valid
        # check if size exist
        if not size:
            return {"message": NOT_FOUND.format("size")}, 401


        # check if productsubcat is in product cat
        print("yes yes --> ", productsubcat.productcat.id , productcat.id)
        if productsubcat.productcat.id != productcat.id:
            return {"message" : NOT_FOUND_IN.format("product sub category", "product category")}, 404
            
        # check if store id is for current user
        return False, 200

    @classmethod
    def put_unique_already_exist(cls, claim, productid, product_data):
        # check user permission, edit and parse data
        product = cls.find_by_id(id=productid)
        store, productcat, productsubcat, size = cls.check_unique_inputs(product_data=product_data)

        # check if product exist
        if not product:
            return None, {"message": NOT_FOUND.format("product")}, 401

        # check if store exist
        if not store:
            return None, {"message": NOT_FOUND.format("store")}, 401

        # check if user is admin or normal user
        if not claim["is_admin"] or not claim["is_root"]  or claim["userid"] != store.user.id:
            return None, {"message": ADMIN_PRIVILEDGE_REQUIRED.format("to post a store")}, 401

        # check if product is in store
        if product.store.id != store.id:
            return None, {"message" : NOT_EQUAL.format("product store id -- " + str(product.store.id ), "storeid -- " + str(store.id))}, 401

        # check productcatid
        # check if productcat exist
        if not productcat:
            return None, {"message": NOT_FOUND.format("productcat")}, 401

        # check product subcat id
        # check if productsubcat insert exist
        if not productsubcat:
            return None, {"message": NOT_FOUND.format("productsubcat")}, 401

        #check if size is valid
        # check if size exist
        if not size:
            return None, {"message": NOT_FOUND.format("size")}, 401


        # check if productsubcat is in product cat
        if productsubcat.productcat.id != productcat.id:
            return None, {"message" : NOT_FOUND_IN.format("product sub category", "product category")}, 404

        return product, False, 200

    @classmethod
    def delete_auth(cls, claim, storeid):
        store = StoreModel.find_by_id(storeid)

        if not store:
            return product, {"message": NOT_FOUND.format("store")}, 401

        if store and not claim["is_admin"] and claim["userid"] != store.user_id:
            return product, {"message": ADMIN_PRIVILEDGE_REQUIRED}, 401
        return product, False, 200

    @classmethod
    def check_foreignkey_exist(cls, store_data):
        user = cls.user.find_by_id(store_data["user_id"])
        return user

# TODO: Do pagenate in response, for product.
# TODO: check if i did put request side of product (i think)
# TODO: check if i did delete auth side of product (i think is checked)
from models.models_helper import *


class ProductColorModel(db.Model, ModelsHelper):
    __tablename__ = "productcol"

    # class variables
    id = db.Column(db.Integer, primary_key=True, unique=True)
    product_id = db.Column(
        db.String(50), db.ForeignKey("product.id"), unique=False, nullable=False
    )
    color_id = db.Column(
        db.Integer, db.ForeignKey("colors.id"), unique=False, nullable=False
    )

    @classmethod
    def check_unique_inputs(cls, productcol_data=None):
        productcol = cls.find_by_productid_and_colorid(
            product_id=productcol_data.get("product_id", None),
            color_id=productcol_data.get("color_id", None),
        )
        product = cls.find_product_by_id(
            product_id=productcol_data.get("product_id", None)
        )
        color = cls.find_color_by_id(color_id=productcol_data.get("color_id", None))
        return productcol, product, color

    @classmethod
    def post_unique_already_exist(cls, claim, productcol_data):
        # check if input don't exist before
        productcol, product, color = cls.check_unique_inputs(
            productcol_data=productcol_data
        )
        user = cls.find_user_by_id(user_id=claim.get("userid", None))

        # check if productcol to be inserted exist
        # check if the product to be inserted is in the user's store
        # check if user is admin or root user
        if not claim or not user or not claim["is_admin"] or not claim["is_root"]:
            return (
                {"message": ADMIN_PRIVILEDGE_REQUIRED.format("post product color")},
                401,
            )
            # check if product to input exist
        if not product:
            return (
                {"message": NOT_FOUND.format("product id", product)},
                400,
            )

        # check if color to input exist
        if not color:
            return (
                {"message": NOT_FOUND.format("color id", color)},
                400,
            )
        if productcol:
            return (
                {
                    "message": ALREADY_EXISTS.format(
                        "product and color",
                        productcol_data.get("product_id", None)
                        + " and "
                        + str(productcol_data.get("color_id", None)),
                    )
                },
                400,
            )  # 400 is for bad request
        return False, 200

    @classmethod
    def put_unique_already_exist(cls, claim, productcolor_id, productcol_data):
        user = cls.find_user_by_id(user_id=claim.get("userid", None))

        # productcol to edit if it exist
        productcolorid_ = cls.find_by_id(id=productcolor_id)

        # check if input don't exist before
        productcolor, product, color = cls.check_unique_inputs(
            productcol_data=productcol_data
        )

        # check if user is admin or root user
        if not claim or not user or not claim["is_admin"] or not claim["is_root"]:
            return (
                None,
                {"message": ADMIN_PRIVILEDGE_REQUIRED.format("edit product color")},
                401,
            )

        # check if user has permission to edit the productcolid and insert productcol
        # check if the productcol to be edited exist
        if not productcolorid_:
            return (
                None,
                {"message": NOT_FOUND.format("productcol id", productcolorid_)},
                400,
            )

        # check if product to input exist
        if not product:
            return (
                None,
                {"message": NOT_FOUND.format("product id", product)},
                400,
            )

        # check if color to input exist
        if not color:
            return (
                None,
                {"message": NOT_FOUND.format("color id", color)},
                400,
            )

        # check if product to be inserted is for current user
        if user:
            if product and product.store.user.id != user.id:
                return (
                    None,
                    {
                        "message": CANNOT_INSERT.format(
                            "product id", "it does not belong to user."
                        )
                    },
                    401,
                )

            # check if productcol to be inserted exist
            # check if the product to be inserted is in the user's store
            if productcolor and productcolor.product.store.user.id != user.id:
                return (
                    None,
                    {
                        "message": ALREADY_EXISTS.format(
                            "product and color",
                            productcol_data.get("product_id", None)
                            + " and "
                            + productcol_data.get("color_id", None),
                        )
                    },
                    400,
                )  # 400 is for bad request
        return productcolor, False, 200

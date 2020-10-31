from models.models_helper import *


class ColorsModel(db.Model, ModelsHelper):
    __tablename__ = "colors"

    # class variables
    id = db.Column(db.Integer, primary_key=True, unique=True)
    desc = db.Column(db.String(256), nullable=False)

    # productcol = db.relationship(
    #     "ProductColorModel",
    #     lazy="dynamic",
    #     backref="colors",
    #     cascade="all, delete-orphan",
    # )

    @classmethod
    def find_by_colordesc(cls, colordesc=None):
        result = cls.query.filter_by(desc=colordesc).first()
        return result

    @classmethod
    def check_unique_inputs(cls, color_data=None):
        desc = cls.find_by_colordesc(colordesc=color_data.get("desc", None))
        return desc

    @classmethod
    def post_unique_already_exist(cls, claim, color_data):
        desc = cls.check_unique_inputs(color_data=color_data)
        if desc:
            return {
                "message": ALREADY_EXISTS.format("product color", color_data["desc"])
            }, 400  # 400 is for bad request
        elif not claim or (claim and (not claim["is_admin"] or not claim["is_root"])):
            return {
                "message": ADMIN_PRIVILEDGE_REQUIRED.format("post product colors")
            }, 401
        return False, 200

    @classmethod
    def put_unique_already_exist(cls, claim, color_id, color_data):
        color = cls.find_by_id(id=color_id)
        desc = cls.check_unique_inputs(color_data=color_data)

        # check color permission, edit and parse data
        if not claim or not claim["is_admin"]:
            return (
                color,
                {"message": ADMIN_PRIVILEDGE_REQUIRED.format("edit product color")},
                401,
            )
        if desc and color and desc.id != color.id:
            return (
                color,
                {"message": ALREADY_EXISTS.format("color", color_data["desc"])},
                400,
            )  # 400 is for bad request
        return color, False, 200

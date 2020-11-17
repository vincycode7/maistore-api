from models.models_helper import *


class ColorsModel(db.Model, ModelsHelper):
    __tablename__ = "colors"

    # class variables
    id = db.Column(db.Integer, primary_key=True, unique=True)
    desc = db.Column(db.String(256), nullable=False)

    productcol = db.relationship(
        "ProductColorModel",
        lazy="dynamic",
        backref="colors",
        cascade="all, delete-orphan",
    )

    @classmethod
    def find_by_colordesc(cls, colordesc=None, get_err="color_err_get_by_desc"):
        try:
            result = cls.query.filter_by(desc=colordesc).first()
        except Exception as e:
            raise ColorException(gettext(get_err).format(e))
        except:
            raise ColorException(gettext(get_err))
        return result

    @classmethod
    def check_unique_inputs(cls, color_data=None, get_err="color_err_get_unique"):
        try:
            desc = cls.find_by_colordesc(colordesc=color_data.get("desc", None))
        except Exception as e:
            raise ColorException(gettext(get_err).format(e))
        except:
            raise ColorException(gettext(get_err))
        return desc

    @classmethod
    def post_unique_already_exist(cls, color_data):
        msg, status_code, _ = ColorsModel.auth_by_admin_root(
            get_err="color_req_ad_priv_to_post"
        )
        if status_code != 200:
            return msg, status_code
        desc = cls.check_unique_inputs(color_data=color_data)
        if desc:
            return {
                "message": gettext("color_already_exist")
            }, 400  # 400 is for bad request
        return False, 200

    @classmethod
    def put_unique_already_exist(cls, color_id, color_data):
        # check color permission, edit and parse data
        msg, status_code, _ = cls.auth_by_admin_root(
            get_err="color_req_ad_priv_to_edit"
        )
        if status_code != 200:
            return msg, status_code

        color = cls.find_by_id(id=color_id)
        desc = cls.check_unique_inputs(color_data=color_data)

        if desc and color and desc.id != color.id:
            return (
                None,
                {"message": gettext("color_already_exist")},
                400,
            )  # 400 is for bad request
        return color, False, 200

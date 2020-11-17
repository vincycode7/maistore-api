from models.models_helper import *
from uuid import uuid4

# helper functions
def create_id(context):
    return "MAISTORE-V1-" + uuid4().hex


class StoreModel(db.Model, ModelsHelper):
    __tablename__ = "store"

    # class variable
    id = db.Column(db.String(50), primary_key=True, unique=True, default=create_id)
    storename = db.Column(db.String(40), unique=True, nullable=False)
    user_id = db.Column(
        db.String(50),
        db.ForeignKey(
            "users.id",
        ),
        nullable=False,
    )
    created = db.Column(
        db.DateTime, index=False, unique=False, nullable=False, default=dt.now
    )
    country = db.Column(db.String(30), nullable=True)
    image = db.Column(db.String(100), nullable=True, default=None)

    # merge (for sqlalchemy to link tables)
    products = db.relationship(
        "ProductModel", lazy="dynamic", backref="store", cascade="all, delete-orphan"
    )
    customers = db.relationship(
        "FavStoreModel", lazy="dynamic", backref="store", cascade="all, delete-orphan"
    )
    orders = db.relationship(
        "CartSystemModel", lazy="dynamic", backref="store", cascade="all, delete-orphan"
    )
    locations = db.relationship(
        "StorelocModel", lazy="dynamic", backref="store", cascade="all, delete-orphan"
    )
    phonenos = db.relationship(
        "StorephoneModel", lazy="dynamic", backref="store", cascade="all, delete-orphan"
    )
    emails = db.relationship(
        "StoreemailModel", lazy="dynamic", backref="store", cascade="all, delete-orphan"
    )

    @classmethod
    def find_by_name(
        cls, storename: str = None, get_err="store_err_find_by_name"
    ) -> "StoreModel":
        try:
            result = cls.query.filter_by(storename=storename).first()
        except Exception as e:
            raise StoreException(gettext(get_err).format(e))
        except:
            raise StoreException(gettext(get_err))
        return result

    @classmethod
    def check_unique_inputs(cls, store_data):
        storename = cls.find_by_name(storename=store_data.get("storename", None))
        user = cls.find_user_by_id(user_id=store_data.get("user_id", None))
        return storename, user

    @classmethod
    def post_unique_already_exist(cls, store_data):
        # check subcat permission, edit and parse data
        msg, status_code, _ = cls.auth_by_admin_root_or_user(
            user_id=store_data.get("user_id"), get_err="store_req_ad_priv_to_post"
        )
        if status_code != 200:
            return msg, status_code

        storename, user = cls.check_unique_inputs(store_data=store_data)

        # check if user id to insert exist
        if not user:
            return {"message": gettext("user_not_found")}, 404

        elif storename:
            return {"message": gettext("store_exist")}, 400  # 400 is for bad request

        return False, 200

    @classmethod
    def put_unique_already_exist(cls, store_id, store_data):
        # check user permission, edit and parse data
        store = cls.find_by_id(id=store_id)
        storename, user = cls.check_unique_inputs(store_data=store_data)

        # check subcat permission, edit and parse data
        msg, status_code, _ = cls.auth_by_admin_root_or_user(
            user_id=store_data.get("user_id"), get_err="store_req_ad_priv_to_edit"
        )
        if status_code != 200:
            return None, msg, status_code

        # check if store exist
        if not store:
            return None, {"message": gettext("store_not_found")}, 404

        # check if user own store
        msg, status_code, _ = cls.auth_by_admin_root_or_user(
            user_id=store.user_id, get_err="store_req_ad_priv_to_edit"
        )
        if status_code != 200:
            return None, msg, status_code

        # check if the user to be filled exist
        if not user:
            return None, {"message": gettext("user_not_found")}, 404

        # check if name exist and if user own's it and if it was the store specified
        if storename and storename.id != store.id:
            return (
                None,
                {"message": gettext("store_exist")},
                400,
            )  # 400 is for bad request
        return store, False, 200

    @classmethod
    def delete_auth(cls, store_id):
        store = StoreModel.find_by_id(store_id)

        if not store:
            return store, {"message": gettext("store_not_found")}, 404

        # check if user own store
        msg, status_code, _ = cls.auth_by_admin_root_or_user(
            user_id=store.user_id, get_err="store_req_ad_priv_to_delete"
        )
        if status_code != 200:
            return None, msg, status_code

        return store, False, 200

    @classmethod
    def check_foreignkey_exist(cls, store_data):
        user = cls.users.find_by_id(store_data["user_id"])
        return user

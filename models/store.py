from models.models_helper import *


class StoreModel(db.Model, ModelsHelper):
    __tablename__ = "store"

    # class variable
    id = db.Column(db.Integer, primary_key=True, unique=True)
    storename = db.Column(db.String(40), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "user.id",
        ),
        nullable=False,
    )
    created = db.Column(
        db.DateTime, index=False, unique=False, nullable=False, default=dt.now
    )
    country = db.Column(db.String(30), nullable=False)

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
    def find_by_name(cls, storename: str = None) -> "StoreModel":
        result = cls.query.filter_by(storename=storename).first()
        return result

    @classmethod
    def check_unique_inputs(cls, store_data):
        storename = cls.find_by_name(storename=store_data["storename"])
        from models.user import UserModel

        user = UserModel.find_by_id(id=store_data["user_id"])
        return storename, user

    @classmethod
    def post_unique_already_exist(cls, claim, store_data):
        if not claim["is_admin"] and claim["userid"] != store_data["userid"]:
            return {"message": ADMIN_PRIVILEDGE_REQUIRED.format("to post a store")}, 401

        storename, user = cls.check_unique_inputs(store_data=store_data)
        if not user:
            return {"message": NOT_FOUND.format("user")}, 400
        elif storename:
            return {
                "message": ALREADY_EXISTS.format("store", store_data["storename"])
            }, 401  # 400 is for bad request
        return False, 200

    @classmethod
    def put_unique_already_exist(cls, claim, storeid, store_data):
        store = cls.find_by_id(id=storeid)
        # check user permission, edit and parse data
        if not claim["is_admin"] and claim["userid"] != store_data["user_id"]:
            return (
                store,
                {"message": ADMIN_PRIVILEDGE_REQUIRED.format("edit user data")},
                401,
            )

        storename, user = cls.check_unique_inputs(store_data=store_data)
        if not user:
            return store, {"message": NOT_FOUND.format("user")}, 400
        elif store and storename and store.storename != storename.storename:
            return (
                store,
                {
                    "message": ALREADY_EXISTS.format(
                        "storename", store_data["storename"]
                    )
                },
                400,
            )  # 400 is for bad request
        return store, False, 200

    @classmethod
    def delete_auth(cls, claim, storeid):
        store = StoreModel.find_by_id(storeid)

        if not store:
            return store, {"message": NOT_FOUND.format("store")}, 401

        if store and not claim["is_admin"] and claim["userid"] != store.user_id:
            return store, {"message": ADMIN_PRIVILEDGE_REQUIRED}, 401
        return store, False, 200

    @classmethod
    def check_foreignkey_exist(cls, store_data):
        user = cls.user.find_by_id(store_data["user_id"])
        return user

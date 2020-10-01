from ma import ma
from models.storephone import StorephoneModel


class StorephoneSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StorephoneModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True

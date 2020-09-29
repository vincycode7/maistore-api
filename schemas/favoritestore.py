from ma import ma
from models.favoritestore import FavStoreModel

class FavStoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FavStoreModel
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True
        include_relationships = True

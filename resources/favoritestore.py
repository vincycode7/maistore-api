from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.favoritestore import FavStoreModel


class FavStoreList(Resource):
    @jwt_required
    def get(self):
        favs = FavStoreModel.find_all()
        if favs:
            return {gettext("favorites"): [fav.json() for fav in favs]}, 201
        return {gettext("message"): gettext("favorite_store_not_found")}, 400

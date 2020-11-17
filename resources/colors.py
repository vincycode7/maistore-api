import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.colors import *
from schemas.colors import ColorsSchema

schema = ColorsSchema()
schema_many = ColorsSchema(many=True)


# class to list all Colors
class ColorList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        colors = ColorsModel.find_all()
        if colors:
            return {"colors": schema_many.dump(colors)}, 201
        return {"message": gettext("color_not_found")}, 404


# class to add colors
class Color(Resource):
    @jwt_required
    def get(self, color_id):
        color = ColorsModel.find_by_id(id=color_id)
        if color:
            return {"color": schema.dump(color)}, 201
        return {"message": gettext("color_not_found")}, 404

    @jwt_required
    def post(self):
        data = schema.load(ColorsModel.get_data_())
        # check if data already exist
        unique_input_error, status = ColorsModel.post_unique_already_exist(data)
        if unique_input_error:
            return unique_input_error, status

        color = ColorsModel(**data)

        # save
        try:
            color.save_to_db()
        except Exception as e:
            print(f"error is {e}")
            return {
                "message": gettext("Internal_server_error")
            }, 500  # Internal server error
        return schema.dump(color), 201

    @jwt_required
    def put(self, color_id):
        data = schema.load(ColorsModel.get_data_())

        # confirm the unique key to be same with the product route
        color, unique_input_error, status = ColorsModel.put_unique_already_exist(
            color_id=color_id, color_data=data
        )

        if unique_input_error:
            return unique_input_error, status

        # if user already exist update the dictionary
        if color:
            for each in data.keys():
                color.__setattr__(each, data[each])

            # save
            try:
                color.save_to_db()
                return schema.dump(color), 201
            except Exception as e:
                print(f"error is {e}")
                return {
                    "message": gettext("Internal_server_error")
                }, 500  # Internal server error
        return {"message": gettext("color_not_found")}, 404

    @jwt_required
    def delete(self, color_id):
        msg, status_code, _ = cls.auth_by_admin_root(
            get_err="color_req_ad_priv_to_edit"
        )
        if status_code != 200:
            return msg, status_code

        color = ColorsModel.find_by_id(id=color_id)
        if color:
            color.delete_from_db()
            return {"message": gettext("color_deleted")}, 200  # 200 ok
        return {"message": gettext("color_not_found")}, 404  # 400 is for bad request

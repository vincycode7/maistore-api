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
        return {"message": NOT_FOUND.format("colors")}, 400


# class to add colors
class Color(Resource):
    @jwt_required
    def get(self, colorid):
        color = ColorsModel.find_by_id(id=colorid)
        if color:
            return {"color": schema.dump(color)}, 201
        return {"message": NOT_FOUND.format("color")}, 400

    @jwt_required
    def post(self):
        claim = get_jwt_claims()
        data = schema.load(ColorsModel.get_data_())

        # check if data already exist
        unique_input_error, status = ColorsModel.post_unique_already_exist(claim, data)
        if unique_input_error:
            return unique_input_error, status

        color = ColorsModel(**data)

        # save
        try:
            color.save_to_db()
        except Exception as e:
            print(f"error is {e}")
            return {
                "message": ERROR_WHILE_INSERTING.format("color")
            }, 500  # Internal server error
        return schema.dump(color), 201

    @jwt_required
    def put(self, colorid):
        claim = get_jwt_claims()
        data = schema.load(ColorsModel.get_data_())

        # confirm the unique key to be same with the product route
        color, unique_input_error, status = ColorsModel.put_unique_already_exist(
            claim=claim, colorid=colorid, color_data=data
        )

        if unique_input_error:
            return unique_input_error, status

        # if user already exist update the dictionary
        if color:
            for each in data.keys():
                color.__setattr__(each, data[each])
            # else:
            #     # check if data already exist
            #     unique_input_error, status = ColorsModel.post_unique_already_exist(claim, data)
            #     if unique_input_error:
            #         return unique_input_error, status
            #     color = ColorsModel(**data)

            # save
            try:
                color.save_to_db()
                return schema.dump(color), 201
            except Exception as e:
                print(f"error is {e}")
                return {
                    "message": ERROR_WHILE_INSERTING.format("color")
                }, 500  # Internal server error
        return {"message": NOT_FOUND.format("color")}, 400  # 400 is for bad request

    @jwt_required
    def delete(self, colorid):
        claim = get_jwt_claims()
        if not claim["is_admin"] or not claim["is_root"]:
            return {"message": ADMIN_PRIVILEDGE_REQUIRED.format("delete color")}, 401
        color = ColorsModel.find_by_id(id=colorid)
        if color:
            color.delete_from_db()
            return {"message": DELETED.format("color")}, 200  # 200 ok
        return {"message": NOT_FOUND.format("color")}, 400  # 400 is for bad request

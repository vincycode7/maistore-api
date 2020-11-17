from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from libs import image_helper
from libs.strings import gettext
from schemas.image import ImageSchema
from models.models_helper import ModelsHelper
from libs.image_helper import IMAGEDELETEEXCEPTION, send_image
import os

image_schema = ImageSchema()
AVATAR_PATH = "Users/user_{}/avatar/"


class UserAvatar(Resource):
    @classmethod
    def get(cls, user_id: int):
        avatar_4_user = ModelsHelper.find_user_by_id(user_id=user_id)
        folder = AVATAR_PATH.format(user_id)  # Users/user_1/images/
        avatar_folder_path = image_helper.get_path(
            filename="", folder=folder)  # static/Users/user_1/images/

        if not avatar_4_user:
            return {"message" : gettext("user_not_found")}, 404

        if not avatar_4_user.image:
            return {"message": gettext("image_not_found")}, 404
        print(send_image(filename=avatar_4_user.image, folder=avatar_folder_path))
        return send_image(filename=avatar_4_user.image, folder=avatar_folder_path)

    @classmethod
    @jwt_required
    def put(cls, user_id: int=None):
        """
        Used to upload an image file.
        It uses JWT to retrieve user information and then saves 
        the image to the user's folder. If there is a filename 
        conflict, it appends a number at the end.
        """

        data = image_schema.load(request.files)  # {"image":FileStorage}
        filename = data["image"].filename

        # check user permission to acces resource
        try:
            err_msg, status_code, _ = ModelsHelper.auth_by_admin_root_or_user(
                user_id=user_id, get_err="user_req_ad_priv_to_change_upload_image")
        except Exception as e:
            print(e)
            return {"message": gettext("Internal_server_error")}, 500

        if status_code != 200:
            return {"message": err_msg}, status_code

        upload_4_user = ModelsHelper.find_user_by_id(user_id=user_id)
        if not upload_4_user:
            return {"message": gettext("user_not_found")}, 404

        folder = AVATAR_PATH.format(user_id)  # Users/user_1/avatar/
        avatar_folder_path = image_helper.get_path(filename="", folder=folder)
        # save the image on disk
        try:
            # check is filename is save to use
            if not image_helper.is_filename_safe(filename):
                return {"message": gettext("image_illegal_filename").format(filename)}, 400

            # save new avatar
            try:
                image_path = image_helper.save_image(
                    data["image"], folder=folder)
            except Exception as e:
                print(e)
                try:
                    image_helper.delete_image_in_dir(
                        folder_path=avatar_folder_path, filename=image_helper.get_basename(image_path))
                except Exception as e:
                    print(e)
                return gettext("image_err_500_saving_image"), 500

            basename = image_helper.get_basename(image_path)

            # delete any existing avatar but not the current avatar
            try:
                image_helper.delete_all_image_in_dir_except(
                    folder_path=avatar_folder_path, filename=basename)
            except IMAGEDELETEEXCEPTION as e:
                print(gettext("image_err_deleting_file").format(e))

            # save image to database
            upload_4_user.__setattr__("image", basename)

            # save to db
            try:
                upload_4_user.save_to_db()
            except Exception as e:
                # delete avatar locally
                try:
                    image_path = image_helper.delete_image_in_dir(
                        folder_path=avatar_folder_path, filename=basename)
                except Exception as e:
                    print(gettext("image_err_deleting_file").format(e))

                return {
                    "message": gettext("Internal_server_error")
                }, 500  # Internal server error
            return {"message": gettext("image_uploaded").format(basename)}, 201
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": gettext("image_illegal_extension").format(extension)}, 400
        except Exception as e:
            print(e)
            return {
                "message": gettext("Internal_server_error")
            }, 500  # Internal server error

    @classmethod
    @jwt_required
    def delete(cls, user_id=None):
        """
        Used to delete an image file.
        It uses JWT to retrieve user information and then delete 
        the image from the user's folder.
        """

        # check user permission to acces resource
        try:
            err_msg, status_code, _ = ModelsHelper.auth_by_admin_root_or_user(
                user_id=user_id, get_err="user_req_ad_priv_to_change_upload_image")
        except Exception as e:
            print(e)
            return {"message": gettext("Internal_server_error")}, 500

        if status_code != 200:
            return {"message": err_msg}, status_code

        delete_4_user = ModelsHelper.find_user_by_id(user_id=user_id)
        if not delete_4_user:
            return {"message": gettext("user_not_found")}, 404

        folder = AVATAR_PATH.format(user_id)  # Users/user_1/images/
        avatar_folder_path = image_helper.get_path(
            filename="", folder=folder)  # static/Users/user_1/images/

        # delete the image on disk
        try:
            # delete avatar locally
            try:
                if not delete_4_user.image:
                    return {"message": gettext("image_not_found")}, 404
                image_path = image_helper.delete_image_in_dir(
                    folder_path=avatar_folder_path, filename=delete_4_user.image)
            except Exception as e:
                print(e)
                return gettext("image_err_500_deleting_image"), 500

            basename = image_helper.get_basename(image_path)

            # delete image from database
            delete_4_user.__setattr__("image", None)

            # save to db
            try:
                delete_4_user.save_to_db()
            except Exception as e:
                print(e)
                return {
                    "message": gettext("Internal_server_error")
                }, 500  # Internal server error
            return {"message": gettext("image_deleted").format(basename)}, 201
        except Exception as e:
            print(e)
            return {
                "message": gettext("Internal_server_error")
            }, 500  # Internal server error

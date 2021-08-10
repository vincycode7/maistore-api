from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from libs import file_helper
from libs.strings import gettext
from schemas.image import ImageSchema
from models.models_helper import ModelsHelper
from libs.file_helper import IMAGEDELETEEXCEPTION, send_user_file
import os

image_schema = ImageSchema()
USER_AVATAR_PATH = "Users/user_{}/avatar/"
STORE_AVATAR_PATH = "Stores/store_{}/avatar/"
PRODUCT_AVATAR_PATH = "Products/product_{}/avatar/"
PRODUCTCAT_AVATAR_PATH = "Productcats/productcat_{}/avatar/"


class UserAvatar(Resource):
    @classmethod
    @jwt_required
    def get(cls, user_id: str):
        avatar_4_user = ModelsHelper.find_user_by_id(user_id=user_id)
        folder = USER_AVATAR_PATH.format(user_id)  # Users/user_1/images/
        avatar_folder_path = file_helper.get_path(
            filename="", folder=folder)  # static/Users/user_1/images/

        if not avatar_4_user:
            return {"message": gettext("user_not_found")}, 404

        if not avatar_4_user.avatar:
            return {"message": gettext("avatar_not_found")}, 404
        try:
            return send_user_file(filename=avatar_4_user.avatar, folder=avatar_folder_path)
        except FileNotFoundError:
            return {"message": gettext("avatar_not_found")}, 404
        except:
            return {"message": gettext("Internal_server_error")}, 500

    @classmethod
    @jwt_required
    def put(cls, user_id: str = None):
        """
        Used to upload an image file.
        It uses JWT to retrieve user information and then saves 
        the image to the user's folder. If there is a filename 
        conflict, it appends a number at the end.
        """

        data = image_schema.load(request.files)  # {"image":FileStorage}
        filename = data["image"].filename

        upload_4_user = ModelsHelper.find_user_by_id(user_id=user_id)
        if not upload_4_user:
            return {"message": gettext("user_not_found")}, 404

        # check user permission to acces resource
        try:
            err_msg, status_code, _ = ModelsHelper.auth_by_admin_root_or_user(
                user_id=user_id, get_err="user_req_ad_priv_to_upload_user_avatar")
        except Exception as e:
            print(e)
            return {"message": gettext("Internal_server_error")}, 500

        if status_code != 200:
            return {"message": err_msg}, status_code

        folder = USER_AVATAR_PATH.format(user_id)  # Users/user_1/avatar/
        avatar_folder_path = file_helper.get_path(filename="", folder=folder)
        # save the image on disk
        try:
            # check is filename is save to use
            if not file_helper.is_filename_safe(filename):
                return {"message": gettext("avatar_illegal_filename").format(filename)}, 400

            # save new avatar
            try:
                avatar_path = file_helper._save_file(
                    data["image"], folder=folder)
            except Exception as e:
                print(e)
                try:
                    file_helper.delete_file_in_dir(
                        folder_path=avatar_folder_path, filename=file_helper.get_basename(avatar_path))
                except Exception as e:
                    print(e)
                return gettext("avatar_err_500_saving_avatar"), 500

            basename = file_helper.get_basename(avatar_path)

            # delete any existing avatar but not the current avatar
            try:
                file_helper.delete_all_file_in_dir_except(
                    folder_path=avatar_folder_path, filename=basename)
            except IMAGEDELETEEXCEPTION as e:
                print(gettext("avatar_err_deleting_file").format(e))

            # save image to database
            print("base base" + basename)
            upload_4_user.__setattr__("avatar", basename)

            # save to db
            try:
                upload_4_user.save_to_db()
            except Exception as e:
                # delete avatar locally
                try:
                    avatar_path = file_helper.delete_file_in_dir(
                        folder_path=avatar_folder_path, filename=basename)
                except Exception as e:
                    print(gettext("avatar_err_deleting_file").format(e))

                return {
                    "message": gettext("Internal_server_error")
                }, 500  # Internal server error
            return {"message": gettext("avatar_uploaded").format(basename)}, 201
        except UploadNotAllowed:
            extension = file_helper.get_extension(data["image"])
            return {"message": gettext("avatar_illegal_extension").format(extension)}, 400
        except Exception as e:
            print(e)
            return {
                "message": gettext("Internal_server_error")
            }, 500  # Internal server error

    @classmethod
    @jwt_required
    def delete(cls, user_id: str = None):
        """
        Used to delete an image file.
        It uses JWT to retrieve user information and then delete 
        the image from the user's folder.
        """
        delete_4_user = ModelsHelper.find_user_by_id(user_id=user_id)
        if not delete_4_user:
            return {"message": gettext("user_not_found")}, 404

        # check user permission to acces resource
        try:
            err_msg, status_code, _ = ModelsHelper.auth_by_admin_root_or_user(
                user_id=user_id, get_err="user_req_ad_priv_to_upload_user_avatar")
        except Exception as e:
            print(e)
            return {"message": gettext("Internal_server_error")}, 500

        if status_code != 200:
            return {"message": err_msg}, status_code

        folder = USER_AVATAR_PATH.format(user_id)  # Users/user_1/images/
        avatar_folder_path = file_helper.get_path(
            filename="", folder=folder)  # static/Users/user_1/images/

        # delete the image on disk
        try:
            # delete avatar locally
            try:
                if not delete_4_user.avatar:
                    return {"message": gettext("avatar_not_found")}, 404
                avatar_path = file_helper.delete_file_in_dir(
                    folder_path=avatar_folder_path, filename=delete_4_user.avatar)
            except FileNotFoundError:
                return {"message": gettext("avatar_not_found")}, 404
            except Exception as e:
                print(e)
                return gettext("avatar_err_500_deleting_avatar"), 500

            basename = file_helper.get_basename(avatar_path)

            # delete image from database
            delete_4_user.__setattr__("avatar", None)

            # save to db
            try:
                delete_4_user.save_to_db()
            except Exception as e:
                return {
                    "message": gettext("Internal_server_error")
                }, 500  # Internal server error
            return {"message": gettext("avatar_deleted").format(basename)}, 201
        except Exception as e:
            print(e)
            return {
                "message": gettext("Internal_server_error")
            }, 500  # Internal server error


class StoreAvatar(Resource):
    @classmethod
    def get(cls, store_id: str):
        avatar_4_store = ModelsHelper.find_store_by_id(store_id=store_id)
        folder = STORE_AVATAR_PATH.format(store_id)  # Stores/store_1/avatar/
        avatar_folder_path = file_helper.get_path(
            filename="", folder=folder)  # static/Stores/store_1/avatar/

        if not avatar_4_store:
            return {"message": gettext("store_not_found")}, 404

        if not avatar_4_store.avatar:
            return {"message": gettext("avatar_not_found")}, 404
        try:
            return send_user_file(filename=avatar_4_store.avatar, folder=avatar_folder_path)
        except FileNotFoundError:
            return {"message": gettext("avatar_not_found")}, 404
        except:
            return {"message": gettext("Internal_server_error")}, 500

    @classmethod
    @jwt_required
    def put(cls, store_id: str = None):
        """
        Used to upload an image file.
        It uses JWT to retrieve user information and then saves 
        the image to the user's folder. If there is a filename 
        conflict, it appends a number at the end.
        """

        data = image_schema.load(request.files)  # {"image":FileStorage}
        filename = data["image"].filename

        upload_4_store = ModelsHelper.find_store_by_id(store_id=store_id)
        if not upload_4_store:
            return {"message": gettext("store_not_found")}, 404

        # check user permission to acces resource
        try:
            err_msg, status_code, _ = ModelsHelper.auth_by_admin_root_or_user(
                user_id=upload_4_store.user_id, get_err="user_req_ad_priv_to_upload_store_avatar")
        except Exception as e:
            return {"message": gettext("Internal_server_error")}, 500

        if status_code != 200:
            return {"message": err_msg}, status_code

        folder = STORE_AVATAR_PATH.format(store_id)  # Stores/store_1/avatar/
        avatar_folder_path = file_helper.get_path(filename="", folder=folder)
        # save the image on disk
        try:
            # check is filename is save to use
            if not file_helper.is_filename_safe(filename):
                return {"message": gettext("avatar_illegal_filename").format(filename)}, 400

            # save new avatar
            try:
                avatar_path = file_helper._save_file(
                    data["image"], folder=folder)
            except Exception as e:
                print(e)
                try:
                    file_helper.delete_file_in_dir(
                        folder_path=avatar_folder_path, filename=file_helper.get_basename(avatar_path))
                except Exception as e:
                    print(e)
                return gettext("avatar_err_500_saving_avatar"), 500

            basename = file_helper.get_basename(avatar_path)

            # delete any existing avatar but not the current avatar
            try:
                file_helper.delete_all_file_in_dir_except(
                    folder_path=avatar_folder_path, filename=basename)
            except IMAGEDELETEEXCEPTION as e:
                print(gettext("avatar_err_deleting_file").format(e))

            # save image to database
            upload_4_store.__setattr__("avatar", basename)

            # save to db
            try:
                upload_4_store.save_to_db()
            except Exception as e:
                # delete avatar locally
                try:
                    avatar_path = file_helper.delete_file_in_dir(
                        folder_path=avatar_folder_path, filename=basename)
                except Exception as e:
                    print(gettext("avatar_err_deleting_file").format(e))

                return {
                    "message": gettext("Internal_server_error")
                }, 500  # Internal server error
            return {"message": gettext("avatar_uploaded").format(basename)}, 201
        except UploadNotAllowed:
            extension = file_helper.get_extension(data["image"])
            return {"message": gettext("avatar_illegal_extension").format(extension)}, 400
        except Exception as e:
            print(e)
            return {
                "message": gettext("Internal_server_error")
            }, 500  # Internal server error

    @classmethod
    @jwt_required
    def delete(cls, store_id=None):
        """
        Used to delete an image file.
        It uses JWT to retrieve user information and then delete 
        the image from the user's folder.
        """
        delete_4_store = ModelsHelper.find_store_by_id(store_id=store_id)
        if not delete_4_store:
            return {"message": gettext("store_not_found")}, 404

        # check user permission to acces resource
        try:
            err_msg, status_code, _ = ModelsHelper.auth_by_admin_root_or_user(
                user_id=delete_4_store.user_id, get_err="user_req_ad_priv_to_upload_store_avatar")
        except Exception as e:
            return {"message": gettext("Internal_server_error")}, 500

        if status_code != 200:
            return {"message": err_msg}, status_code

        delete_4_user = ModelsHelper.find_user_by_id(
            user_id=delete_4_store.user_id)
        if not delete_4_user:
            return {"message": gettext("user_not_found")}, 404

        folder = STORE_AVATAR_PATH.format(
            delete_4_store.id)  # Stores/store_1/avatar/
        avatar_folder_path = file_helper.get_path(
            filename="", folder=folder)  # static/Stores/store_1/avatar/

        # delete the image on disk
        try:
            # delete avatar locally
            try:
                if not delete_4_store.avatar:
                    return {"message": gettext("avatar_not_found")}, 404
                print(avatar_folder_path, delete_4_store.avatar)
                avatar_path = file_helper.delete_file_in_dir(
                    folder_path=avatar_folder_path, filename=delete_4_store.avatar)
            except FileNotFoundError:
                return {"message": gettext("avatar_not_found")}, 404
            except Exception as e:
                return gettext("avatar_err_500_deleting_avatar"), 500

            basename = file_helper.get_basename(avatar_path)

            # delete image from database
            delete_4_store.__setattr__("avatar", None)

            # save to db
            try:
                delete_4_store.save_to_db()
            except Exception as e:
                print(e)
                return {
                    "message": gettext("Internal_server_error")
                }, 500  # Internal server error
            return {"message": gettext("avatar_deleted").format(basename)}, 201
        except Exception as e:
            print(e)
            return {
                "message": gettext("Internal_server_error")
            }, 500  # Internal server error


class ProductAvatar(Resource):
    @classmethod
    def get(cls, product_id: str):
        avatar_4_product = ModelsHelper.find_product_by_id(
            product_id=product_id)
        folder = PRODUCT_AVATAR_PATH.format(
            product_id)  # Stores/store_1/avatar/
        avatar_folder_path = file_helper.get_path(
            filename="", folder=folder)  # static/Products/product_1/avatar/

        if not avatar_4_product:
            return {"message": gettext("product_not_found")}, 404

        if not avatar_4_product.avatar:
            return {"message": gettext("avatar_not_found")}, 404
        try:
            return send_user_file(filename=avatar_4_product.avatar, folder=avatar_folder_path)
        except FileNotFoundError:
            return {"message": gettext("avatar_not_found")}, 404
        except:
            return {"message": gettext("Internal_server_error")}, 500

    @classmethod
    @jwt_required
    def put(cls, product_id: str = None):
        """
        Used to upload an image file.
        It uses JWT to retrieve user information and then saves 
        the image to the user's folder. If there is a filename 
        conflict, it appends a number at the end.
        """

        data = image_schema.load(request.files)  # {"image":FileStorage}
        filename = data["image"].filename

        upload_4_product = ModelsHelper.find_product_by_id(
            product_id=product_id)
        if not upload_4_product:
            return {"message": gettext("product_not_found")}, 404

        # check user permission to acces resource
        try:
            err_msg, status_code, _ = ModelsHelper.auth_by_admin_root_or_user(
                user_id=upload_4_product.store.user_id, get_err="user_req_ad_priv_to_upload_product_avatar")
        except Exception as e:
            return {"message": gettext("Internal_server_error")}, 500

        if status_code != 200:
            return {"message": err_msg}, status_code

        folder = PRODUCT_AVATAR_PATH.format(
            product_id)  # Products/product_1/avatar/
        avatar_folder_path = file_helper.get_path(filename="", folder=folder)
        # save the image on disk
        try:
            # check is filename is save to use
            if not file_helper.is_filename_safe(filename):
                return {"message": gettext("avatar_illegal_filename").format(filename)}, 400

            # save new avatar
            try:
                avatar_path = file_helper._save_file(
                    data["image"], folder=folder)
            except Exception as e:
                print(e)
                try:
                    file_helper.delete_file_in_dir(
                        folder_path=avatar_folder_path, filename=file_helper.get_basename(avatar_path))
                except Exception as e:
                    print(e)
                return gettext("avatar_err_500_saving_avatar"), 500

            basename = file_helper.get_basename(avatar_path)

            # delete any existing avatar but not the current avatar
            try:
                file_helper.delete_all_file_in_dir_except(
                    folder_path=avatar_folder_path, filename=basename)
            except IMAGEDELETEEXCEPTION as e:
                print(gettext("avatar_err_deleting_file").format(e))

            # save image to database
            upload_4_product.__setattr__("avatar", basename)

            # save to db
            try:
                upload_4_product.save_to_db()
            except Exception as e:
                # delete avatar locally
                try:
                    avatar_path = file_helper.delete_file_in_dir(
                        folder_path=avatar_folder_path, filename=basename)
                except Exception as e:
                    print(gettext("avatar_err_deleting_file").format(e))

                return {
                    "message": gettext("Internal_server_error")
                }, 500  # Internal server error
            return {"message": gettext("avatar_uploaded").format(basename)}, 201
        except UploadNotAllowed:
            extension = file_helper.get_extension(data["image"])
            return {"message": gettext("avatar_illegal_extension").format(extension)}, 400
        except Exception as e:
            print(e)
            return {
                "message": gettext("Internal_server_error")
            }, 500  # Internal server error

    @classmethod
    @jwt_required
    def delete(cls, product_id=None):
        """
        Used to delete an image file.
        It uses JWT to retrieve user information and then delete 
        the image from the user's folder.
        """
        delete_4_product = ModelsHelper.find_product_by_id(
            product_id=product_id)
        if not delete_4_product:
            return {"message": gettext("product_not_found")}, 404

        # check user permission to acces resource
        try:
            err_msg, status_code, _ = ModelsHelper.auth_by_admin_root_or_user(
                user_id=delete_4_product.store.user_id, get_err="user_req_ad_priv_to_delete_store_avatar")
        except Exception as e:
            return {"message": gettext("Internal_server_error")}, 500

        if status_code != 200:
            return {"message": err_msg}, status_code

        delete_4_user = ModelsHelper.find_user_by_id(
            user_id=delete_4_product.store.user_id)
        if not delete_4_user:
            return {"message": gettext("user_not_found")}, 404

        folder = PRODUCT_AVATAR_PATH.format(
            delete_4_product.id)  # Products/product_1/avatar/
        avatar_folder_path = file_helper.get_path(
            filename="", folder=folder)  # static/Products/product_1/avatar/

        # delete the image on disk
        try:
            # delete avatar locally
            try:
                if not delete_4_product.avatar:
                    return {"message": gettext("avatar_not_found")}, 404
                print(avatar_folder_path, delete_4_product.avatar)
                avatar_path = file_helper.delete_file_in_dir(
                    folder_path=avatar_folder_path, filename=delete_4_product.avatar)
            except FileNotFoundError:
                return {"message": gettext("avatar_not_found")}, 404
            except Exception as e:
                return gettext("avatar_err_500_deleting_avatar"), 500

            basename = file_helper.get_basename(avatar_path)

            # delete image from database
            delete_4_product.__setattr__("avatar", None)

            # save to db
            try:
                delete_4_product.save_to_db()
            except Exception as e:
                print(e)
                return {
                    "message": gettext("Internal_server_error")
                }, 500  # Internal server error
            return {"message": gettext("avatar_deleted").format(basename)}, 201
        except Exception as e:
            print(e)
            return {
                "message": gettext("Internal_server_error")
            }, 500  # Internal server error


class ProductCatAvatar(Resource):
    @classmethod
    def get(cls, productcat_id: int):
        avatar_4_productcat = ModelsHelper.find_productcat_by_id(
            productcat_id=productcat_id)
        folder = PRODUCTCAT_AVATAR_PATH.format(
            productcat_id)  # Productcats/productcat_1/avatar/
        avatar_folder_path = file_helper.get_path(
            filename="", folder=folder)  # static/Productcats/productcat_1/avatar/

        if not avatar_4_productcat:
            return {"message": gettext("product_cat_not_found")}, 404

        if not avatar_4_productcat.avatar:
            return {"message": gettext("avatar_not_found")}, 404
        try:
            return send_user_file(filename=avatar_4_productcat.avatar, folder=avatar_folder_path)
        except FileNotFoundError:
            return {"message": gettext("avatar_not_found")}, 404
        except:
            return {"message": gettext("Internal_server_error")}, 500

    @classmethod
    @jwt_required
    def put(cls, productcat_id: int = None):
        """
        Used to upload an image file.
        It uses JWT to retrieve user information and then saves 
        the image to the user's folder. If there is a filename 
        conflict, it appends a number at the end.
        """
        data = image_schema.load(request.files)  # {"image":FileStorage}
        filename = data["image"].filename

        upload_4_productcat = ModelsHelper.find_productcat_by_id(
            productcat_id=productcat_id)
        if not upload_4_productcat:
            return {"message": gettext("product_cat_not_found")}, 404

        # check user permission to acces resource
        try:
            err_msg, status_code, _ = ModelsHelper.auth_by_admin_root(
                get_err="user_req_ad_priv_to_upload_product_cat_avatar")
        except Exception as e:
            return {"message": gettext("Internal_server_error")}, 500

        if status_code != 200:
            return {"message": err_msg}, status_code

        folder = PRODUCTCAT_AVATAR_PATH.format(
            productcat_id)  # Productcats/productcat_1/avatar/
        avatar_folder_path = file_helper.get_path(filename="", folder=folder)
        # save the image on disk
        try:
            # check is filename is save to use
            if not file_helper.is_filename_safe(filename):
                return {"message": gettext("avatar_illegal_filename").format(filename)}, 400

            # save new avatar
            try:
                avatar_path = file_helper._save_file(
                    data["image"], folder=folder)
            except Exception as e:
                print(e)
                try:
                    file_helper.delete_file_in_dir(
                        folder_path=avatar_folder_path, filename=file_helper.get_basename(avatar_path))
                except Exception as e:
                    print(e)
                return gettext("avatar_err_500_saving_avatar"), 500

            basename = file_helper.get_basename(avatar_path)

            # delete any existing avatar but not the current avatar
            try:
                file_helper.delete_all_file_in_dir_except(
                    folder_path=avatar_folder_path, filename=basename)
            except IMAGEDELETEEXCEPTION as e:
                print(gettext("avatar_err_deleting_file").format(e))

            # save image to database
            upload_4_productcat.__setattr__("avatar", basename)

            # save to db
            try:
                upload_4_productcat.save_to_db()
            except Exception as e:
                # delete avatar locally
                try:
                    avatar_path = file_helper.delete_file_in_dir(
                        folder_path=avatar_folder_path, filename=basename)
                except Exception as e:
                    print(gettext("avatar_err_deleting_file").format(e))

                return {
                    "message": gettext("Internal_server_error")
                }, 500  # Internal server error
            return {"message": gettext("avatar_uploaded").format(basename)}, 201
        except UploadNotAllowed:
            extension = file_helper.get_extension(data["image"])
            return {"message": gettext("avatar_illegal_extension").format(extension)}, 400
        except Exception as e:
            print(e)
            return {
                "message": gettext("Internal_server_error")
            }, 500  # Internal server error

    @classmethod
    @jwt_required
    def delete(cls, productcat_id: int = None):
        """
        Used to delete an image file.
        It uses JWT to retrieve user information and then delete 
        the image from the user's folder.
        """
        delete_4_productcat = ModelsHelper.find_productcat_by_id(
            productcat_id=productcat_id)
        if not delete_4_productcat:
            return {"message": gettext("product_cat_not_found")}, 404

        # check user permission to acces resource
        try:
            err_msg, status_code, _ = ModelsHelper.auth_by_admin_root(
                get_err="user_req_ad_priv_to_delete_product_cat_avatar")
        except Exception as e:
            return {"message": gettext("Internal_server_error")}, 500

        if status_code != 200:
            return {"message": err_msg}, status_code

        folder = PRODUCTCAT_AVATAR_PATH.format(
            delete_4_productcat.id)  # Productcats/productcat_1/avatar/
        avatar_folder_path = file_helper.get_path(
            filename="", folder=folder)  # static/Productcats/productcat_1/avatar/

        # delete the image on disk
        try:
            # delete avatar locally
            try:
                if not delete_4_productcat.avatar:
                    return {"message": gettext("avatar_not_found")}, 404
                avatar_path = file_helper.delete_file_in_dir(
                    folder_path=avatar_folder_path, filename=delete_4_productcat.avatar)
            except FileNotFoundError:
                return {"message": gettext("avatar_not_found")}, 404
            except Exception as e:
                return gettext("avatar_err_500_deleting_avatar"), 500

            basename = file_helper.get_basename(avatar_path)

            # delete image from database
            delete_4_productcat.__setattr__("avatar", None)

            # save to db
            try:
                delete_4_productcat.save_to_db()
            except Exception as e:
                print(e)
                return {
                    "message": gettext("Internal_server_error")
                }, 500  # Internal server error
            return {"message": gettext("avatar_deleted").format(basename)}, 201
        except Exception as e:
            print(e)
            return {
                "message": gettext("Internal_server_error")
            }, 500  # Internal server error

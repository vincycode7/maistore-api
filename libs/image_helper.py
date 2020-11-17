"""
    Library that contains functions to manioulate images.
"""

import os
import re
from typing import Union
from werkzeug.datastructures import FileStorage
from flask_uploads import UploadSet, IMAGES
from flask import send_file
IMAGE_SET = UploadSet("images", IMAGES)  # set name and allowed extensions


class IMAGEDELETEEXCEPTION(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class FileHelper:
    pass


class LocalStoreHelper:
    pass


class CloudinaryHelper:
    pass


class S3BucketHelper:
    pass


def send_image(folder: str, filename: str, name: str = None):
    if name:
        return send_file(filename_or_fp=name)
    name = folder+filename
    return send_file(filename_or_fp=name)


def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    """ Takes a filestorage and saves it to a folder"""
    return IMAGE_SET.save(image, folder, name)


def get_path(filename: str = None, folder: str = None) -> str:
    """ Takes an image name, folder and returns a full path"""
    return IMAGE_SET.path(filename, folder)


def find_all_image_in_dir(folder_path: str) -> Union[str, None]:
    return os.listdir(folder_path)


def delete_image_in_dir(folder_path: str, filename: str):
    filename = get_basename(str(filename))
    image_path = folder_path+filename
    try:
        os.remove(image_path)
    except Exception as e:
        raise IMAGEDELETEEXCEPTION(e)
    return image_path


def delete_all_image_in_dir(folder_path: str) -> None:
    all_images = find_all_image_in_dir(folder_path=folder_path)

    for image_base in all_images:
        try:
            os.remove(folder_path+image_base)
        except Exception as e:
            raise IMAGEDELETEEXCEPTION(e)
    return folder_path


def delete_all_image_in_dir_except(folder_path: str, filename: str):
    all_images = find_all_image_in_dir(folder_path=folder_path)
    image_path = folder_path+filename
    for image_base in all_images:
        if image_base == filename:
            continue
        try:
            os.remove(folder_path+image_base)
        except Exception as e:
            raise IMAGEDELETEEXCEPTION(e)
    return image_path


def find_image_any_format(filename: str, folder: str) -> Union[str, None]:
    """
    Takes a filename and returns an image on any of the accepted formats.
    """
    for _format in IMAGES:
        image = f"{filename}.{_format}"
        image_path = IMAGE_SET.path(filename=image, folder=folder)
        if os.path.isfile(image_path):
            return image_path
    return None


def find_image_curr_format(img_basename: str, folder: str) -> Union[str, None]:
    """
    Takes a filename and returns an image on any of the accepted formats.
    """
    image_path = IMAGE_SET.path(filename=img_basename, folder=folder)
    if os.path.isfile(image_path):
        return image_path
    return None


def _retrieve_filename(file_: Union[str, FileStorage]) -> str:
    """ 
        Takes a filestorage and returns the file name.
        Allows our function to call this with both file 
        names and FileStorage and always gets back a 
        filename.
    """
    if isinstance(file_, FileStorage):
        return file_.filename
    return file_


def is_filename_safe(file_: Union[str, FileStorage]) -> bool:
    """ check our regex and return whether the string matches or not"""
    filename = _retrieve_filename(file_)
    allowed_format = "|".join(IMAGES)  # png|svg|jpg|jpeg|png
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
    return re.match(regex, filename) is not None


def get_basename(file_: Union[str, FileStorage]) -> str:
    """ 
        Returns fullname of image in the path.
        get_basename("some/folder/image.jpg") returns "image.jpg"
    """
    filename = _retrieve_filename(file_)
    return os.path.split(filename)[1]


def get_image_name(file_: Union[str, FileStorage]) -> str:
    """ 
        Returns image name without the extension.
        get_basename("some/folder/image.jpg") returns "image"
    """
    filename = _retrieve_filename(file_)
    filename = os.path.split(filename)[1]
    return filename.split(".")[0]


def get_extension(file_: Union[str, FileStorage]) -> str:
    """ 
        Returns file extension 
        get_extension("image.jpg") returns ".jpg"
    """
    filename = _retrieve_filename(file_)
    return os.path.splitext(filename)[1]

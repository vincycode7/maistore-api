"""
    Library that contains functions to manipulate images.
"""

import os
import re
from typing import Union
from werkzeug.datastructures import FileStorage
from flask_uploads import ( 
                                UploadSet, IMAGES, AUDIO, 
                                DOCUMENTS, TEXT, DATA, 
                                SCRIPTS, ARCHIVES, EXECUTABLES
                            )
import flask_uploads
from flask import send_file



VIDEOS = tuple('mp4'.split())
flask_uploads.DEFAULTS = flask_uploads.DEFAULTS + VIDEOS

FILETYPE_DICT = {
                    "image" : "IMAGES",
                    "video" : "VIDEOS",
                    "audio" : "AUDIO",
                    "document" : "DOCUMENTS",
                    "script" : "SCRIPTS",
                    "archive" : "ARCHIVES",
                    "executable" : "EXECUTABLES",
                    "text" : "TEXT",
                    "data" : "DATA"
}

IMAGE_SET = UploadSet("image", IMAGES)  # set name and allowed extensions
VIDEO_SET = UploadSet("video", VIDEOS)  # set name and allowed extensions
AUDIO_SET = UploadSet("audio", AUDIO)  # set name and allowed extensions
DOCUMENT_SET = UploadSet("document", DOCUMENTS)  # set name and allowed extensions
SCRIPT_SET = UploadSet("script", SCRIPTS)  # set name and allowed extensions
ARCHIVE_SET = UploadSet("archive", ARCHIVES)  # set name and allowed extensions
EXECUTABLE_SET = UploadSet("executable", EXECUTABLES)  # set name and allowed extensions
TEXT_SET = UploadSet("text", TEXT)  # set name and allowed extensions
DATA_SET = UploadSet("data", DATA)  # set name and allowed extensions

TYPESET_DICT = {
                    "image" : "IMAGE",
                    "video" : "VIDEO",
                    "audio" : "AUDIO",
                    "document" : "DOCUMENT",
                    "script" : "SCRIPT",
                    "archive" : "ARCHIVE",
                    "executable" : "EXECUTABLE",
                    "text" : "TEXT",
                    "data" : "DATA"
}

class IMAGEDELETEEXCEPTION(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class VIDEODELETEEXCEPTION(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class AUDIODELETEEXCEPTION(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class DOCUMENTDELETEEXCEPTION(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class SCRIPTDELETEEXCEPTION(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class ARCHIVEDELETEEXCEPTION(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class EXECUTABLEDELETEEXCEPTION(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class TEXTDELETEEXCEPTION(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class DATADELETEEXCEPTION(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class INVALIDFILEFORMAT(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class INVALIDFILETYPE(Exception):
    def __init__(self, message: str):
        super().__init__(message)

TYPE_EXEPTION_DICT = {
                    "image" : "IMAGE",
                    "video" : "VIDEO",
                    "audio" : "AUDIO",
                    "document" : "DOCUMENT",
                    "script" : "SCRIPT",
                    "archive" : "ARCHIVE",
                    "executable" : "EXECUTABLE",
                    "text" : "TEXT",
                    "data" : "DATA"
}
class FileHelper:
    pass


class LocalStoreHelper:
    pass


class CloudinaryHelper:
    pass


class S3BucketHelper:
    pass

# function to choose the file format
def choose_format_exception(file_type, err=None):
    file_type = file_type.lower()
    if file_type in TYPE_EXEPTION_DICT.keys():
        raise globals()[f"{TYPE_EXEPTION_DICT[file_type]}ELETEEXCEPTION"](err)
    else:
        raise INVALIDFILETYPE

# function to send user a file
def send_user_file(folder: str, filename: str, name: str = None):
    if name:
        return send_file(filename_or_fp=name)
    name = folder+filename
    return send_file(filename_or_fp=name)

# save a file in db
def _save_file(file_: FileStorage, folder: str = None, name: str = None, file_type: str ="image") -> str:
    """ Takes a filestorage and saves it to a folder"""
    file_type = file_type.lower()
    if file_type in TYPESET_DICT.keys():
        return globals()[f"{TYPESET_DICT[file_type]}_SET"].save(file_, folder, name)
    else:
        raise INVALIDFILETYPE

# get a path to a file
def get_path(filename: str = None, folder: str = None, file_type: str ="image") -> str:
    """ Takes a file name, folder and returns a full path"""

    file_type = file_type.lower()
    if file_type in TYPESET_DICT.keys():
        return globals()[f"{TYPESET_DICT[file_type]}_SET"].path(filename, folder)
    else:
        raise INVALIDFILETYPE

# find all files in a directory
def find_all_files_in_dir(folder_path: str) -> Union[str, None]:
    return os.listdir(folder_path)

# delete a file in the dir
def delete_file_in_dir(folder_path: str, filename: str, file_type: str ="image"):
    filename = get_basename(str(filename))
    file_path = folder_path+filename
    try:
        os.remove(file_path)
    except FileNotFoundError:
        raise FileNotFoundError
    except Exception as e:
        print(e)
        file_type = file_type.lower()
        choose_format_exception(file_type=file_type,err=e)
    return file_path

# delete all file in a dir
def delete_all_file_in_dir(folder_path: str, file_type: str ="image") -> None:
    all_files = find_all_files_in_dir(folder_path=folder_path)

    for file_base in all_files:
        try:
            os.remove(folder_path+file_base)
        except Exception as e:
            choose_format_exception(file_type=file_type,err=e)
    return folder_path

# delete all file in a dir except
def delete_all_file_in_dir_except(folder_path: str, filename: str, file_type: str ="image"):
    all_files = find_all_files_in_dir(folder_path=folder_path)
    file_path = folder_path+filename
    for file_base in all_files:
        if file_base == filename:
            continue
        try:
            os.remove(folder_path+file_base)
        except Exception as e:
            choose_format_exception(file_type=file_type,err=e)
    return file_path


def find_file_any_format(filename: str, folder: str, file_type: str ="image") -> Union[str, None]:
    """
    Takes a filename and returns an image on any of the accepted formats.
    """
    if file_type in FILETYPE_DICT.keys():
        for _format in globals()[f"{FILETYPE_DICT[file_type]}"]:
            file_ = f"{filename}.{_format}"
            file_path = globals()[f"{TYPESET_DICT[file_type]}_SET"].path(filename=file_, folder=folder)
            if os.path.isfile(file_path):
                return file_path
    else:
        raise INVALIDFILETYPE
    return None


def find_file_curr_format(file_basename: str, folder: str, file_type: str ="image") -> Union[str, None]:
    """
    Takes a filename and returns an image on any of the accepted formats.
    """
    if file_type in FILETYPE_DICT.keys():
        file_path = globals()[f"{TYPESET_DICT[file_type]}_SET"].path(filename=file_basename, folder=folder)
        if os.path.isfile(file_path):
            return file_path
    else:
        raise INVALIDFILETYPE
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


def get_file_name(file_: Union[str, FileStorage], file_type: str ="image") -> str:
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

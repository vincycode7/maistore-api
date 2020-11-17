import os

DEBUG = os.environ["DEBUG"]
PORT = os.environ["PORT"]
# CREATE_ROOT=os.environ["CREATE_ROOT"]
SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URI"]
CLOUDINARY_URL = os.environ["CLOUDINARY_URL"]
UPLOADED_IMAGES_DEST = os.path.join(
    os.environ["UPLOADED_IMAGES_DEST"], "static")
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ["SQLALCHEMY_TRACK_MODIFICATIONS"]
PROPAGATE_EXCEPTIONS = os.environ["PROPAGATE_EXCEPTIONS"]
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
SECRET_KEY = os.environ["APP_SECRET_KEY"]
JWT_BLACKLIST_ENABLED = os.environ["JWT_BLACKLIST_ENABLED"]
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
DEFAULT_PARSERS = [
    "flask.ext.api.parsers.JSONParser",
    "flask.ext.api.parsers.URLEncodedParser",
    "flask.ext.api.parsers.MultiPartParser",
]
CORS_HEADERS = "Content-Type"

# storage_options: local, aws, cloudinary

# storage_options: local, aws, cloudinary
import os
# basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
DEBUG = os.environ["DEBUG"]
PORT = os.environ["PORT"]
CLOUDINARY_URL = os.environ["CLOUDINARY_URL"]
UPLOADED_IMAGE_DEST = os.path.join(os.environ["UPLOADED_IMAGES_DEST"], "static")
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

# class Config(object):
#     DEBUG = False
#     TESTING = False
#     CSRF_ENABLED = True
#     SECRET_KEY = 'this-really-needs-to-be-changed'
#     SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
#     DEBUG = os.environ["DEBUG"]
#     PORT = os.environ["PORT"]
#     SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
#     CLOUDINARY_URL = os.environ["CLOUDINARY_URL"]
#     UPLOADED_IMAGES_DEST = os.path.join(os.environ["UPLOADED_IMAGES_DEST"], "static")
#     SQLALCHEMY_TRACK_MODIFICATIONS = os.environ["SQLALCHEMY_TRACK_MODIFICATIONS"]
#     PROPAGATE_EXCEPTIONS = os.environ["PROPAGATE_EXCEPTIONS"]
#     JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
#     SECRET_KEY = os.environ["APP_SECRET_KEY"]
#     JWT_BLACKLIST_ENABLED = os.environ["JWT_BLACKLIST_ENABLED"]
#     JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
#     DEFAULT_PARSERS = [
#         "flask.ext.api.parsers.JSONParser",
#         "flask.ext.api.parsers.URLEncodedParser",
#         "flask.ext.api.parsers.MultiPartParser",
#     ]
#     CORS_HEADERS = "Content-Type"

# class ProductionConfig(Config):
#     DEBUG = False


# class StagingConfig(Config):
#     DEVELOPMENT = True
#     DEBUG = True


# class DevelopmentConfig(Config):
#     DEVELOPMENT = True
#     DEBUG = True


# class TestingConfig(Config):
#     TESTING = True

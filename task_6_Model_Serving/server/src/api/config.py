# api/config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False
    ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg'}
    MAX_CONTENT_LENGTH = 1024 * 1024 * 10 # 10 MB
    LOGS_DIR = 'outputs/logs/'

    @staticmethod
    def init_app(app):
        pass

class S3StorageConfig(Config):
    REGION_NAME = os.environ.get("REGION_NAME")
    ENDPOINT_URL = os.environ.get("ENDPOINT_URL")
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    BUCKET_NAME = os.environ.get("BUCKET_NAME")


class LocalStorageConfig(Config):
    UPLOAD_FOLDER = os.environ.get(
        "UPLOAD_FOLDER"
    ) or os.path.join(os.path.dirname(os.path.dirname(basedir)), "uploads", "images")


class DevelopmentConfig(LocalStorageConfig):
    DEBUG = True
    HOST = ""


class StagingConfig(LocalStorageConfig):
    TESTING = True
    HOST = ""


class ProductionConfig(LocalStorageConfig):
    HOST = ""


env_config = {
    "development": DevelopmentConfig,
    "staging": StagingConfig,
    "production": ProductionConfig,
}

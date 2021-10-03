# api/config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    UPLOAD_FOLDER = os.environ.get(
        "UPLOAD_FOLDER"
    ) or os.path.join(os.path.dirname(os.path.dirname(basedir)), "uploads", "images")
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    HOST = ""


class StagingConfig(Config):
    TESTING = True
    HOST = ""


class ProductionConfig(Config):
    HOST = ""


env_config = {
    "development": DevelopmentConfig,
    "staging": StagingConfig,
    "production": ProductionConfig,
}

# api/app.py
from flask import Flask
from flask_restful import Api
from api.docs import Docs

api = Api()


def create_app(config_name):
    from api.config import env_config
    from api.resources.routes import initialize_routes

    app = Flask(__name__)

    app.config.from_object(env_config[config_name])
    api.init_app(app)

    docs_ = Docs(config_name)
    docs_.init_swagger(app)

    return app

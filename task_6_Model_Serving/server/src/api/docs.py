from api.config import env_config
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder


class Docs:
    def __init__(self, config_name):
        self.template = {
            "swagger": "2.0",
            "info": {
                "title": "Omdena Tea Leaf Quality Prediction API",
                "description": "API for the tea leaf quality prediction",
                "version": "0.1.1",
                "contact": {
                    "name": "Omdena AI",
                    "url": "https://omdena.com/omdena-chapter-page-srilanka/",
                }
            },
            # "host": env_config[config_name].HOST,  # overrides localhost:500
            # "basePath": "/api",  # base bash for blueprint registration
            "schemes": [LazyString(lambda: 'https' if request.is_secure else 'http')]
        }
        self.swagger_config = {
            "title": "Omdena Tea Leaf Prediction API",
            "uiversion": 3,
            "headers": [
            ],
            "specs": [
                {
                    "endpoint": 'apispec_1',
                    "route": '/apispec_1.json',
                    "rule_filter": lambda rule: True,  # all in
                    "model_filter": lambda tag: True,  # all in
                }
            ],
            "static_url_path": "/flasgger_static",
            # "static_folder": "static",  # must be set by user
            "swagger_ui": True,
            "specs_route": "/api/docs/"
        }

    def init_swagger(self, app):
        # Set the custom Encoder (Inherit it if you need to customize)
        app.json_encoder = LazyJSONEncoder

        Swagger(app, template=self.template, config=self.swagger_config)

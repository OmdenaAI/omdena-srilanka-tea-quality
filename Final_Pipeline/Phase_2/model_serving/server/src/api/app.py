# api/app.py
from flask import Flask
from flask_restful import Api
from webargs.flaskparser import abort, parser
from werkzeug import exceptions
from logging.config import dictConfig
import os

from api.docs import Docs
from api.utils import errors

api = Api()


def create_app(config_name):
    from api.config import env_config
    from api.resources.routes import initialize_routes
    from pathlib import Path

    log_dir = Path(env_config[config_name].LOGS_DIR, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            },
            'file_handler': {
                'class': 'logging.FileHandler',
                'filename': f'{log_dir}/api.log',
                'formatter': 'default',
                'level':'INFO'
            }
        },
        'root': {
            'level':'DEBUG',
            'handlers': ['wsgi', 'file_handler']
        }
    })

    app = Flask(__name__)

    app.config.from_object(env_config[config_name])
    api.init_app(app)

    docs_ = Docs(config_name)
    docs_.init_swagger(app)

    app.register_error_handler(exceptions.NotFound, errors.handle_404_errors)

    app.register_error_handler(
        exceptions.InternalServerError, errors.handle_server_errors
    )

    app.register_error_handler(exceptions.BadRequest, errors.handle_400_errors)

    app.register_error_handler(FileNotFoundError, errors.handle_400_errors)

    app.register_error_handler(TypeError, errors.handle_400_errors)

    app.register_error_handler(KeyError, errors.handle_404_errors)

    app.register_error_handler(AttributeError, errors.handle_400_errors)

    app.register_error_handler(ValueError, errors.handle_400_errors)

    app.register_error_handler(AssertionError, errors.handle_400_errors)

    @parser.error_handler
    def handle_request_parsing_error(
        err, req, schema, *, error_status_code, error_headers
    ):
        """webargs error handler that uses Flask-RESTful's abort function to return
        a JSON error response to the client.
        """
        abort(error_status_code, errors=err.messages)

    return app


if __name__ == "__main__":
    env = os.getenv("FLASK_ENV")
    # print(env)
    application = create_app(env)
    application.run()

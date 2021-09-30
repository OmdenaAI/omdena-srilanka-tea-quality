from flask import Flask
from flask_restful import Api
from .resources.routes import initialize_routes

app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION')

api = Api(app)

initialize_routes(api)

if __name__ == "__main__":
    app.run()

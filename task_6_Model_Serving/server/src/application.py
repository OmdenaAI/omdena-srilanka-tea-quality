# main.py
import os

from api.app import create_app

env = os.getenv("FLASK_ENV")
# print(env)
application = create_app(env)

if __name__ == "__main__":
    application.run()

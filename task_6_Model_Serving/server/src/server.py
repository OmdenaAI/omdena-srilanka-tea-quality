# main.py
import os

from api.app import create_app

env = os.getenv("FLASK_ENV")
# print(env)
app = create_app(env)

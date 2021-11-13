# app.py
import os

from api.app import create_app

env = os.getenv("FLASK_ENV")
# print(env)
app = create_app(env)

if __name__ == "__main__":
    app.run()
    # app.run(host="0.0.0.0", port=5000)
    # app.run(port=5001)

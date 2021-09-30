from flask import jsonify
from flask_restful import Resource


class TestsApi(Resource):
    def get(self):
        return jsonify({'tests': ["test1", "test2"]})

from flask import request, jsonify, Response
from flask_restful import Resource


class InferencesApi(Resource):
    def post(self):
        return '', 200



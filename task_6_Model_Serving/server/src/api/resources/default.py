from flask_restful import Resource
from http import HTTPStatus

from api.app import api


class DefaultResource(Resource):
    """
    Handle default route
    """

    def get(self):
        """
        Default api route handler
        ---
        tags:
        - Home
        responses:
          200:
            description: Simple welcome message
            schema:
              properties:
                status:
                  type: string
                  description: Status of the request
                msg:
                  type: string
                  description: Status msg
        """
        return {
            'status': 'success',
            'msg': 'Welcome to the Tea Leaf API!'
        }, HTTPStatus.OK


api.add_resource(DefaultResource, '/api/', endpoint='home')

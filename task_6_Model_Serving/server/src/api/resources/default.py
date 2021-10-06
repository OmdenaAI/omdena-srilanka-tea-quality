from flask_restful import Resource
from flasgger import swag_from
from http import HTTPStatus

from api.app import api


class DefaultResource(Resource):
  """
  Default route handler
  """
  @swag_from("../docs/default/get.yml")
  def get(self):
    return 'Welcome to the Tea Leaf API!', HTTPStatus.OK


api.add_resource(DefaultResource, '/api/', endpoint='home')

'''
Inferences endpoint Resource script. It exposes '/inferences' endpoint with a POST method.
It accepts an image file and returns the result of prediction from CNN model.
'''
from flask import request, Response, current_app
from flask_restful import Resource, reqparse
from flasgger import swag_from
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from http import HTTPStatus
import os
import imghdr

from api.app import api
from api.config import env_config
from api.utils.storage import Storage
from models.predictor import Predictor

# Parser to parse the POST request
parser = reqparse.RequestParser()
parser.add_argument('file',
                    type=FileStorage,
                    location='files',
                    required=True)


class InferencesResource(Resource):
  """
  InferencesApi Resource to handle POST request on '/inferences' endpoint.
  """

  def __init__(self, **kwargs):
    self.allowed_exts = current_app.config['ALLOWED_EXTENSIONS']
    self.logger = kwargs.get('logger')

    # print(self.allowed_exts)
    self.storage_handler = Storage()
    self.predictor = Predictor()

  @swag_from("../docs/inference/post.yml")
  def post(self):
    # Parse the request arguments
    args = parser.parse_args()
    # Validation on 'file' argument in the request
    if args['file'] == "":
      return self.__get_error_status__('No file found'), HTTPStatus.BAD_REQUEST

    # read image file from the stream
    uploaded_file = args['file']
    filename = secure_filename(uploaded_file.filename).lower()
    if filename != '':
      # print(filename)
      file_ext = os.path.splitext(filename)[1]
      # print(file_ext)
      if file_ext not in self.allowed_exts or \
        file_ext != self.__validate_image__(uploaded_file.stream):
        return self.__get_error_status__('Invalid file'), HTTPStatus.BAD_REQUEST
    self.storage_handler.save_file(
      uploaded_file, filename, request.mimetype)

    result = self.predictor.predict(uploaded_file)
    # TODO: Prepare response from the result above.

    # Return response json
    return {
      'status': 'success',
      'msg': 'image uploaded',
      'data': {}
    }, HTTPStatus.OK

  def __get_error_status__(self, error_msg):
    return {
      'status': 'error',
      'msg': error_msg
    }
  
  def __validate_image__(self, stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
      return None
    return '.' + (format if format != 'jpeg' else 'jpg')


api.add_resource(InferencesResource, '/api/inferences')

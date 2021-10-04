'''
Inferences endpoint Resource script. It exposes '/inferences' endpoint with a POST method.
It accepts an image file and returns the result of prediction from CNN model.
'''
from flask import request, Response, current_app
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
from http import HTTPStatus
import imghdr

from api.app import api
from api.config import env_config

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
        # print(kwargs)
        # conf = env_config[kwargs.get('config_name')]
        self.upload_folder = current_app.config['UPLOAD_FOLDER']
        self.allowed_exts = current_app.config['ALLOWED_EXTENSIONS']
        self.logger = kwargs.get('logger')

        # print(self.upload_folder)
        # print(self.allowed_exts)

    def post(self):
        """
        Upload image to get inference from model
        ---
        tags:
        - Inference
        consumes:
        - multipart/form-data  
        parameters:
        - name: file
          required: true
          in: formData
          type: file
          description: Upload your file.
        responses:
          400:
            description: Bad request
            schema:
              properties:
                status:
                  type: string
                  description: Status of the request
                msg:
                  type: string
                  description: Error msg of the prediction
          200:
            description: Status of the uploaded image
            schema:
              properties:
                status:
                  type: string
                  description: Status of the request
                msg:
                  type: string
                  description: Status msg of the prediction
        """

        # Parse the request arguments
        args = parser.parse_args()
        # Validation on 'file' argument in the request
        if args['file'] == "":
            return {
                'status': 'error',
                'msg': 'No file found'
            }, HTTPStatus.BAD_REQUEST

        # read image file from the stream
        uploaded_file = args['file']
        filename = secure_filename(uploaded_file.filename).lower()
        if filename != '':
            # print(filename)
            file_ext = os.path.splitext(filename)[1]
            # print(file_ext)
            if file_ext not in self.allowed_exts or \
                    file_ext != self.__validate_image__(uploaded_file.stream):
                return {
                    'status': 'error',
                    'msg': 'Invalid file'
                }, HTTPStatus.BAD_REQUEST
        uploaded_file.save(os.path.join(self.upload_folder, filename))
        # TODO: Add logic to call model methods
        # ...

        # Return response json
        return {
            'status': 'success',
            'msg': 'image uploaded'
        }, HTTPStatus.OK

    def __validate_image__(self, stream):
        header = stream.read(512)
        stream.seek(0)
        format = imghdr.what(None, header)
        if not format:
            return None
        return '.' + (format if format != 'jpeg' else 'jpg')


api.add_resource(InferencesResource, '/api/inferences')

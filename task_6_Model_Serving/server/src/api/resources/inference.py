'''
Inferences endpoint Resource script. It exposes '/inferences' endpoint with a POST method.
It accepts an image file and returns the result of prediction from CNN model.
'''
from flask import request, Response, current_app
from flask_restful import Resource, reqparse
import werkzeug
import os
from http import HTTPStatus

from api.app import api
from api.config import env_config

# Parser to parse the POST request
parser = reqparse.RequestParser()
parser.add_argument('file',
                    type=werkzeug.datastructures.FileStorage,
                    location='files',
                    required=True)


class InferencesResource(Resource):
    """
    InferencesApi Resource to handle POST request on '/inferences' endpoint.
    """

    def __init__(self, **kwargs):
        print(kwargs)
        #conf = env_config[kwargs.get('config_name')]
        self.upload_folder = current_app.config['UPLOAD_FOLDER']
        self.allowed_exts = current_app.config['ALLOWED_EXTENSIONS']
        self.logger = kwargs.get('logger')

    def post(self):
        """
        Upload image to get inference from model
        ---
        responses:
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
        img = args['file']
        if img:
            # Static filename
            file_name = 'up_img.jpg'
            # Save the image into 'Upload_folder' directory
            img.save(os.path.join(self.upload_folder, file_name))
            # TODO: Add logic to call model methods
            # ...

            # Return response json
            return {
                'status': 'success',
                'msg': 'image uploaded'
            }, HTTPStatus.OK
        # Return error json
        return {
            'status': 'error',
            'msg': 'Something went wrong'
        }, HTTPStatus.BAD_REQUEST


api.add_resource(InferencesResource, '/api/inferences')

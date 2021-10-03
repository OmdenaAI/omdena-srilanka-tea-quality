'''
Inferences endpoint Resource script. It exposes '/inferences' endpoint with a POST method.
It accepts an image file and returns the result of prediction from CNN model.
'''
from flask import request, jsonify, Response
from flask_restful import Resource, reqparse
import werkzeug
import os

UPLOAD_FOLDER = 'uploads/images'

# Parser to parse the POST request
parser = reqparse.RequestParser()
parser.add_argument('file',
                    type=werkzeug.datastructures.FileStorage,
                    location='files',
                    required=True)


class InferencesApi(Resource):
    '''
    InferencesApi Resource to handle POST request on '/inferences' endpoint.
    '''

    def post(self):
        '''
        POST method handler on InferencesApi Resource
        '''

        # Parse the request arguments
        args = parser.parse_args()
        # Validation on 'file' argument in the request
        if args['file'] == "":
            return {
                'data': '',
                'message': 'No file found',
                'status': 'error'
            }

        # read image file from the stream
        img = args['file']
        if img:
            print(type(img))
            print(img)
            # Static filename
            file_name = 'up_img.jpg'
            # Save the image into 'Upload_folder' directory
            img.save(os.path.join(UPLOAD_FOLDER, file_name))
            # TODO: Add logic to call model methods
            # ...

            # Return response json
            return {
                'data': '',
                'message': 'image uploaded',
                'status': 'success'
            }
        # Return error json
        return {
            'data': '',
            'message': 'Something went wrong',
            'status': 'error'
        }

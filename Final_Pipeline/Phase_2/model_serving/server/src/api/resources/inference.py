'''
Inferences endpoint Resource script. It exposes '/inferences' endpoint with a POST method.
It accepts an image file and returns the result of prediction from CNN model.
'''
from flask import request, Response, current_app, jsonify
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
from http import HTTPStatus
import imghdr
import logging

from api.app import api
from api.config import env_config
from api.utils.storage import Storage
from detect import Detector
from classify import ClassifierPrediction, TeaLeavesClassifier

# Parser to parse the POST request
parser = reqparse.RequestParser()
parser.add_argument('file',
                    type=FileStorage,
                    location='files',
                    required=True)

class InferenceResult:
  def __init__(self, status:str, msg:str, predictions:ClassifierPrediction=None) -> None:
      self.status = status
      self.msg = msg
      self.predictions = predictions
  
  def serialize(self):
    return {
      'status': self.status,
      'msg': self.msg,
      'predictions': self.predictions.serialize()
    }

class InferencesResource(Resource):
    """
    InferencesApi Resource to handle POST request on '/inferences' endpoint.
    """

    def __init__(self, **kwargs):
        self.allowed_exts = current_app.config['ALLOWED_EXTENSIONS']
        self.logger = kwargs.get('logger')

        # print(self.allowed_exts)
        self.storage_handler = Storage()

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
                predictions:
                  properties:
                    type:
                      type: string
                      description: Type of the tea leaf (Fresh or Withered)
                      example: 'Fresh'
                    categories:
                      properties:
                        best:
                          type: number
                          description: Percentage of category 'Best'
                        below_best:
                          type: number
                          description: Percentage of category 'Below_Best'
                        poor:
                          type: number
                          description: Percentage of category 'Poor'
                    
                  
        """

        # Parse the request arguments
        args = parser.parse_args()
        # Validation on 'file' argument in the request
        if args['file'] == "":
          self.logger.warning('No file found')
          return InferenceResult('error','No file found').serialize(), HTTPStatus.BAD_REQUEST

        # read image file from the stream
        uploaded_file = args['file']
        filename = secure_filename(uploaded_file.filename).lower()
        self.logger.debug(f"Raw filename='{uploaded_file.filename}', Secure filename='{filename}'")
        if filename == "":
          self.logger.warning(f"No secure filename found for raw filename='{uploaded_file.filename}'")
          return InferenceResult('error','No file found').serialize(), HTTPStatus.BAD_REQUEST
        
        file_ext = os.path.splitext(filename)[1]
        self.logger.debug(f"File extension='{file_ext}'")
        is_file_ext_valid = file_ext in self.allowed_exts
        is_file_valid_image = file_ext == self.__validate_image__(uploaded_file.stream)
        if (not is_file_ext_valid) or (not is_file_valid_image):
          self.logger.warning(f"Invalid file extension={is_file_ext_valid}")
          self.logger.warning(f"Invalid image file={is_file_valid_image}")
          return InferenceResult('error','Invalid file').serialize(), HTTPStatus.BAD_REQUEST
        
        # Step 1: Save file
        upload_file_path = self.storage_handler.save_file(
            uploaded_file, filename, request.mimetype)
        self.logger.info(f"Step-1: Uploaded file path='{upload_file_path}'")
        # Step 2: Detect tea leaves from the uploaded file
        detector = Detector(self.logger, file_path=upload_file_path)
        self.logger.debug(f"Step-2: Detect options='{detector.options}'")
        detected_dir = detector.detect()
        self.logger.info(f"Step-2: Detected dir='{detected_dir}'")
        # Step 3: Classify each detected tea leaf image
        classifier = TeaLeavesClassifier(detected_dir)
        predictions = classifier.predictions()
        self.logger.info(f"Step-3: Classifier predictions='{predictions}'")

        # Return response json
        '''
        Result:
        {
          'status'        : '',
          'msg'           : '',
          'predictions'   : {
            'type'        : 'Withered',
            'categories'  : {
              'Best'      : 60.0,
              'Below Best': 15.0,
              'Poor'      : 25.0
            }
          }
        }
        '''
        return InferenceResult('success','image processed', predictions).serialize(), HTTPStatus.OK


    def __validate_image__(self, stream):
        header = stream.read(512)
        stream.seek(0)
        format = imghdr.what(None, header)
        if not format:
            return None
        return '.' + (format if format != 'jpeg' else 'jpg')


api.add_resource(InferencesResource, '/api/inferences', resource_class_kwargs={'logger': logging.getLogger()})

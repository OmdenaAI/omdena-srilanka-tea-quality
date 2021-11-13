from flask import current_app
# import boto3
import os
from pathlib import Path


# class S3Storage:
#     def __init__(self):
#         conf = current_app.config
#         if conf['DEBUG']:
#             raise Exception('Unexpected environment')

#         self.client = boto3.client('s3')
#         self.bucket_name = conf['BUCKET_NAME']

#     def save_file(self, file, filename, content_type):
#         try:
#             self.client.put_object(Body=file,
#                                    Bucket=self.bucket_name,
#                                    Key=filename,
#                                    ContentType=content_type)
#         except:
#             raise Exception('File could not be stored.')


class LocalStorage:
    def __init__(self):
        conf = current_app.config
        # if not conf['DEBUG']:
        #     raise Exception('Unexpected environment')
        if not os.path.exists(conf['UPLOAD_FOLDER']):
            Path(conf['UPLOAD_FOLDER'], exist_ok=True).mkdir(parents=True, exist_ok=True)
        if not os.path.exists(conf['UPLOAD_FOLDER']):
            raise Exception(f"Upload folder({conf['UPLOAD_FOLDER']}) doesn't exist.")
        self.upload_folder = conf['UPLOAD_FOLDER']

    def save_file(self, file, filename, content_type):
        try:
            filepath = os.path.join(self.upload_folder, filename)
            file.save(filepath)
            return filepath
        except:
            raise Exception('File could not be stored.')


class Storage:
    def __init__(self):
        conf = current_app.config
        if True: # conf['DEBUG']:
            self.storage_handler = LocalStorage()
        else:
            raise Exception("Only local storage is defined.")
            # self.storage_handler = S3Storage()

    def save_file(self, file, filename, content_type):
        return self.storage_handler.save_file(file, filename, content_type)

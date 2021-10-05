from flask import current_app
import boto3
import os


class S3Storage:
    def __init__(self):
        conf = current_app.config
        if conf['DEBUG']:
            raise Exception('Unexpected environment')

        self.client = boto3.client('s3')
        self.bucket_name = conf['BUCKET_NAME']

    def save_file(self, file, filename, content_type):
        try:
            self.client.put_object(Body=file,
                                   Bucket=self.bucket_name,
                                   Key=filename,
                                   ContentType=content_type)
        except:
            raise Exception('File could not be stored.')


class LocalStorage:
    def __init__(self):
        conf = current_app.config
        # print(conf)
        if not conf['DEBUG']:
            raise Exception('Unexpected environment')
        self.upload_folder = conf['UPLOAD_FOLDER']

    def save_file(self, file, filename, content_type):
        try:
            file.save(os.path.join(self.upload_folder, filename))
        except:
            raise Exception('File could not be stored.')


class Storage:
    def __init__(self):
        conf = current_app.config
        if conf['DEBUG']:
            self.storage_handler = LocalStorage()
        else:
            self.storage_handler = S3Storage()

    def save_file(self, file, filename, content_type):
        self.storage_handler.save_file(file, filename, content_type)

# Server Side

<img src="ServerArchitecture .JPG">

## Expose Model As An API

1. Model Trainig will happen in server(i.e. where ever training of model is done is refered as server here)
2. Model can be saved with .h5, .pkl, .sav
3. Hosting the model in server side using Flask Framework
4. Now Flask API can be consumend by mobile app.
5. Connect with S3 bucket to save the output of for data archival

## Flask Api Deployment in EC2 instance AWS

1. Flask code
2. Run and check in local
3. Create AWS account
4. Create EC2 instance
5. Download putty and putty gen
6. Generate private key with putty gen
7. Download WinSCP(to copy and paste in cloud instance)
8. Update the port in flask code(make use you have 0.0.0.0 and 8080 as your default port
9. Install the librabies by connecting through putty
10. Run python3 app.py
11. Get the exicution url from the ec2 instance and verify it

## Deploy to Elastic Beanstalk Instance

```shell
cd task_6_model_serving/server/src
# Remove __pycache__/ folders from each subdirectory in src.
zip -r task-6-server-api-6bec1bc8ba53ac389e353f7e2d4d5c238d8db359.zip .
```

- Go to AWS ElasticBeanstalk instance
- Go to `Omdenatealeafqualitypredapi-env-manual` environment
- Add the following environment vars:
  - BUCKET_NAME = <S3 bucket name>
  - FLASK_DEBUG = 0
  - FLASK_ENV = staging
- Click on `Upload and Deploy` button
- Choose the zip file created in the above process
- Click "Deploy"

**Test using ~/api/docs/ url**

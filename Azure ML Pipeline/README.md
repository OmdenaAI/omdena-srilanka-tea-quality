# Omdena SriLanka Chapter

This repo contains the Flask API to expose model and get predictions.

## Expose Model As An API

1. Model Trainig will happen in server(i.e. where ever training of model is done is refered as server here)
2. Model can be saved with .h5, .pkl, .sav
3. Hosting the model in server side using Flask Framework
4. Now Flask API can be consumend by mobile app.

## Flask Api Deployment in Azure App service

1. Flask code
1. Run and check in local
1. Create Azure App service
1. Run python3 app.py
1. Get the execution url from the App service instance and verify it

## Deploy to Elastic Beanstalk Instance

```shell
cd task_6_model_serving/server/src
# Remove __pycache__/ folders from each subdirectory in src.
zip -r task-6-server-api-6bec1bc8ba53ac389e353f7e2d4d5c238d8db359.zip .
```

- Go to AWS ElasticBeanstalk instance
- Go to `Omdenatealeafqualitypredapi-env-manual` environment
- Add following environment vars:
  - BUCKET_NAME = <S3 bucket name>
  - FLASK_DEBUG = 0
  - FLASK_ENV = staging
- Click on `Upload and Deploy` button
- Choose zip file created in above process
- Click "Deploy"

**Test using ~/api/docs/ url**

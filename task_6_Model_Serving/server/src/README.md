# Omdena SriLanka Chapter

This repo contains the Flask API to expose model and get predictions.

## Expose Model As An API

1. Model Trainig will happen in server(i.e. where ever training of model is done is refered as server here)
2. Model can be saved with .h5, .pkl, .sav
3. Hosting the model in server side using Flask Framework
4. Now Flask API can be consumend by mobile app.

## Set up local environment

1. Clone the repository in local directory
   ```shell
   git clone https://github.com/OmdenaAI/omdena-srilanka-tea-quality.git
   ```
1. Change directory
   ```shell
   cd omdena-srilanka-tea-quality/task_6_Model_Serving/server/src/
   ```
1. Create a virtual environment using `pip`
   ```shell
   python3 -m venv sl-tea-leaf-env
   ```
1. Activate the virtual environment
   + On Windows:
     ```powershell
     .\sl-tea-leaf-env\bin\activate
     ```
   + On Linux or Mac-OS:
     ```shell
     source sl-tea-leaf-env/bin/activate
     ```
1. Upgrade pip to the latest
   ```shell
   pip install --upgrade pip
   ```
1. Install all dependencies from `requirements.txt` file
   ```shell
   pip install -r requirements.txt
   ```
1. Set environment variables for Flask to run
   + On Windows, add environment variables via UI
     + FLASK_ENV=development
     + FLASK_APP=app.py
   + On Linux or Mac-OS:
     ```shell
     export FLASK_ENV=development
     export FLASK_APP=app.py
     ```
1. Run FLASK API
   ```shell
   flask run
   ```
1. Access the [Swagger UI](http://127.0.0.1:5000/api/docs/) page
1. Predictions  
   Run from another shell after changing directory to `omdena-srilanka-tea-quality/task_6_Model_Serving/server/src/`
   ```shell
   curl -F file=@assets/samples/Low_Withered_Best.jpg http://127.0.0.1:5000/api/inferences
   ```
1. Check log files  
   + Log files are created in `outputs/logs/` directory
   + Log file is named as `api.log`

## Deployment in Azure App service

1. Follow steps in [Set up local environment](#set-up-local-environment) to set up your local environment and test it in local
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

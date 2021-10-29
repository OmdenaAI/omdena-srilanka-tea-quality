# Omdena SriLanka Chapter - Flask API

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

1. Follow steps in [Set up local environment](#set-up-local-environment) to test it in local
1. Create Azure App service
1. In Azure App service's Deployment center, connect GitHub repo. It will add a GitHub action workflow file in the repo.
1. After the deployment is successful, get the service url from the App service overview and verify by browsing `<service-url>/api/docs/`

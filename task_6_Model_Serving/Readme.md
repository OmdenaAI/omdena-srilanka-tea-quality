# Model Serving

In this task, we'll be using the built model (in Phase-1) to predict the quality of Tea leaves. In order to use the model, we have divided the task into 2 parts:

- Server
- Client

## Server

In this sub-task, we've created **Python Flask API** endpoints which can be used to consume the model and make predictions on the input. The Flask API is hosted on **AWS Sagemaker** service which helps in building the pipeline to serve the model.

The source code can be found [here](task_6_model_serving/src/).

### Usage

In order to run this task in your local or any other machine, follow these steps:

```shell
$ git clone https://github.com/OmdenaAI/omdena-srilanka-tea-quality.git
$ cd omdena-srilank-tea-quality/task_6_model_serving/src/
$ pip install -r requirements.txt
$ python basic_flask.py
```

## Resources

[REST vs RESTful](https://blog.ndepend.com/rest-vs-restful/)

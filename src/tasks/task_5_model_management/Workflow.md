# First Step

We can create a *dataset.py* in which we can load the data, process the data, and log dataset parameters. I also had added dummy *dataset.py* file inside this directory.

# Second Step

We can create a *train_data.py* file in which we will train our data and use any model for prediction.

# Third Step

Now here comes the step of deploying the model. We can deploy the model in two different ways.

- Locally in MLflow
- Integrating with AWS Sagemaker

As we have decided we are going to use AWS sagemaker for deploying, so let's just only focus on Integrating with AWS Sagemaker one.

For doing deployment using AWS sagemaker we need to build a prediction container that we can push to Amazon ECR (docker registry service) and this is what sagemaker will use to create the endpoint and load the model.

***let's Build the Container***

This task would have been much more tedious if we were not going to use MLflow/Azure Databricks. In MLflow we can create the container way easier than others.

```python
mlflow sagemaker build-and-push-container
```

As the name speaks itself, it's gonna make python environment inside the container and it's going to push it to one of our ECR repositories. It's the vanilla container which will already install all the required library as soon as you will run it for once. We don't need to do it more than once.

***Now let's deply it***

It's again a single line of code

```python
mlflow sagemaker deploy -a $APP_NAME -m $MODEL_PATH -e $ROLE --region-name $REGION
```

# Step 4

Now here comes the task of giving prediction, so we will use *predict_model.py* here.This is what the sagemaker will run for us and will give the prediction back to app.


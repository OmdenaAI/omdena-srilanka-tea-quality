import json
import joblib
import numpy as np
import io
import argparse
from PIL import Image
import torchvision.transforms as transforms
import torch
from azureml.core.model import Model
# Called when the service is loaded
def init():
    global model
    # Get the path to the deployed model file and load it
    model_path =  Model.get_model_path('Torch-Classifier-model',1)
    model = torch.load(model_path,map_location='cpu')
    model.eval()
# Called when a request is received
def run(input_data):
    input_data = int(torch.tensor(json.loads(input_data)['data']))

    # get prediction
    with torch.no_grad():
        output = model(input_data)
        classes = ["Fresh_Below_Best","Fresh_Best","Fresh_Poor","Withered_Below_Best","Withered_Best","Withered_Poor"]
        softmax = nn.Softmax(dim=1)
        pred_probs = softmax(output).numpy()[0]
        index = torch.argmax(output, 1)
        result = {"label": classes[index], "probability": str(pred_probs[index])}
    return result
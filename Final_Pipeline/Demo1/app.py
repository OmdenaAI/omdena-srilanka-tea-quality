from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH ='fresh_model_densenet121.h5'
fresh_model = load_model(MODEL_PATH)

MODEL_PATH ='withered_model_densenet121.h5'
withered_model = load_model(MODEL_PATH)



def fresh_model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    x=x/255
    x = np.expand_dims(x, axis=0)
   
    predict = model.predict(x)
    preds = np.argmax(predict, axis=1)
    #"(" + str((np.count_nonzero(predict == 3)/(len(predict)*len(predict[0])))*100) + ")"
    if preds == 0:
        preds = "Low Fresh - Below Best"
    elif preds == 1:
        preds = "Low Fresh - Best"
    else:
        preds = "Low Fresh - Poor"
    return preds #+  " (" + str(predict[0][np.argmax(predict[0])]*100) + "%)"

def withered_model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224)) #Corn_Blight (1002)

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    x=x/255
    x = np.expand_dims(x, axis=0)
   
    predict = model.predict(x)
    preds = np.argmax(predict, axis=1)
    #str((np.count_nonzero(predict == 1)/(len(predict)*len(predict[0])))*100)
    if preds == 0:
        preds = "Low Withered - Below Best"
    elif preds == 1:
        preds = "Low Withered - Best"
    else:
        preds = "Low Withered - Poor"
    return preds #+  " (" + str(predict[0][np.argmax(predict[0])]*100) + "%)"



@app.route('/', methods=['GET'])
def home():
    # Main page
    return render_template('home.html')

@app.route('/fresh_model', methods=['GET'])
def fresh_index():
    # Banana Leaf Classification Page
    return render_template('fresh_index.html')

@app.route('/withered_model', methods=['GET'])
def withered_index():
    # Plant Disease Data Page
    return render_template('withered_index.html')




@app.route('/fresh_model/predict', methods=['GET', 'POST'])
def fresh_upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'Uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        result = fresh_model_predict(file_path, fresh_model)
        return result
    return None

@app.route('/withered_model/predict', methods=['GET', 'POST'])
def withered_upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'Uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        result = withered_model_predict(file_path, withered_model)
        return result
    return None



if __name__ == '__main__':
    app.run(debug=True)

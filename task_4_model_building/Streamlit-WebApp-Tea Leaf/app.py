# Importing Libraries
import streamlit as st
import io
import numpy as np
from PIL import Image 
import tensorflow as tf
import json
import os
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import efficientnet.tfkeras as efn
from model import withered_model, fresh_model


# Loading Model
fresh_model = fresh_model()
withered_model = withered_model()

# Title and Description
st.title('Omdena Tea Leaf Classification')
st.write("Just Upload Your Leaf Image and Get Predictions")
st.write("")
choice = st.selectbox("Select Option",[
    "Withered Category",
    "Fresh Category"
])

gpus = tf.config.experimental.list_physical_devices("GPU")

if gpus:
    tf.config.experimental.set_memory_growth(gpus[0], True)

if choice == "Withered Category":


    # Upload the image
    uploaded_file = st.file_uploader("Choose a Image file", type=["png", "jpg"])


    predictions_map = {0:"Is Below Best", 1:"Is Best", 2:"Is Poor"}

    if uploaded_file is not None:

       image = Image.open(io.BytesIO(uploaded_file.read()))
   
       st.image(image, use_column_width=True)

       # Image Preprocessing
       resized_image = np.array(image.resize((224, 224)))/255.

       # Adding batch dimension
       image_batch = resized_image[np.newaxis, :, :, :]

       # Getting the predictions fom the model
       predictions_arr = withered_model.predict(image_batch)

       predictions = np.argmax(predictions_arr)

       result_text = f"The Tea Leaf {predictions_map[predictions]} With {int(predictions_arr[0][predictions]*100)}% Probability"

       if predictions == 0:
           st.success(result_text)
       else:
           st.error(result_text)
           
elif choice == "Fresh Category":
    # Upload the image
    uploaded_file = st.file_uploader("Choose a Image file", type=["png", "jpg"])


    predictions_map = {0:"Is Below Best", 1:"Is Best", 2:"Is Poor"}

    if uploaded_file is not None:

       image = Image.open(io.BytesIO(uploaded_file.read()))
   
       st.image(image, use_column_width=True)

       # Image Preprocessing
       resized_image = np.array(image.resize((224, 224)))/255.

       # Adding batch dimension
       image_batch = resized_image[np.newaxis, :, :, :]

       # Getting the predictions fom the model
       predictions_arr = fresh_model.predict(image_batch)

       predictions = np.argmax(predictions_arr)

       result_text = f"The Tea Leaf {predictions_map[predictions]} With {int(predictions_arr[0][predictions]*100)}% Probability"

       if predictions == 0:
           st.success(result_text)
       else:
           st.error(result_text)

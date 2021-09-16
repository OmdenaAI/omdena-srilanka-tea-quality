# Import libraries
import numpy as np
import requests
from PIL import ImageDraw, ImageFont, Image
from tqdm import tqdm
from pathlib import Path

classes = ['Below-Best', 'Best', 'Poor']

# pass image into classifier model
def predict(image, model):
    predictions = model.predict(image)
    class_idx = np.argmax(predictions)
    print(predictions)
    return classes[class_idx]

# use deepstack wrapper to connect detection model for detection
def get_leaves(image):
    image_data = image.getvalue()
    response = requests.post("http://localhost:80//v1/vision/custom/tea_leaves",files={"image":image_data}).json()
    return response, len(response['predictions']) # returns detections and number of detections 


def annotate_leaves(image, response):   
	# convert image to RGB format
    image = image.convert('RGB')
	# create imagedraw object
    draw = ImageDraw.Draw(image)
	# create font
    roboto_font = ImageFont.truetype(str(Path(__file__).resolve().parent /  'Roboto-Bold.ttf'), 40)

	# annotate every detection found and labels them
    for  detection in tqdm(response["predictions"], total=len(response['predictions'])):
            x_min = detection['x_min']
            y_min = detection['y_min']
            x_max = detection['x_max']
            y_max = detection['y_max']

            label = detection['label']

            draw.rectangle((x_min, y_min, x_max, y_max), outline=(230, 57, 70), width=7)
            draw.text((x_min, y_min-50), text=label, font=roboto_font, fill=(242, 92, 84))

    
    del draw
    return image 


def predict_leaves(image, response, model, size=(224, 224)):
	# convert image to RGB format    
    image = image.convert('RGB')
	# create imagedraw object
    draw = ImageDraw.Draw(image)
	# create font
    roboto_font = ImageFont.truetype(str(Path(__file__).resolve().parent /  'Roboto-Bold.ttf'), 40)
    
	# crop detected leaves and pass into classifier for classification, returns annotation with class label
    for  detection in tqdm(response["predictions"], total=len(response['predictions'])):
            x_min = detection['x_min']
            y_min = detection['y_min']
            x_max = detection['x_max']
            y_max = detection['y_max']

            label = detection['label']

            leaf = image.crop((x_min,y_min,x_max,y_max))
            leaf = leaf.resize(size, Image.ANTIALIAS)
            leaf = np.asarray(leaf)
            leaf = leaf[np.newaxis, ...]

            pred = predict(leaf, model)


            draw.rectangle((x_min, y_min, x_max, y_max), outline=(230, 57, 70), width=7)
            draw.text((x_min, y_min-50), text=pred, fill=(0, 41, 107), font=roboto_font)
            
            
    
    del draw
    return image
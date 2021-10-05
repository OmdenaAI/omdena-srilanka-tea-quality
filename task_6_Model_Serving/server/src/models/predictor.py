from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from flask import current_app


class Predictor:
    def __init__(self):
        model_filepath = current_app.config['MODEL_FILE']
        print(model_filepath)
        try:
            self.model = load_model(model_filepath)
        except:
            raise Exception('Could not load the model')

    def predict(self, image_file):
        img = image.load_img(image_file, target_size=(224, 224))
        img_arr = image.img_to_array(img)
        preprocessed = self.__preprocess__(img_arr)
        return self.__inference__(preprocessed)

    def __preprocess__(self, img_arr):
        # Scaling
        x = img_arr/255
        x = np.expand_dims(x, axis=0)
        return x

    def __inference__(self, img_arr_preprocessed):
        print(img_arr_preprocessed.shape)
        predict = self.model.predict(img_arr_preprocessed)
        print(predict)

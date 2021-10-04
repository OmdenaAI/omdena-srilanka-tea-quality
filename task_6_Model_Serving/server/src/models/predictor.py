class Predictor:
    def __init__(self):
        pass

    def predict(self, image_file):
        # TODO: Convert image_file to numpy array
        img_arr = None
        preprocessed = self.__preprocess__(img_arr)
        return self.__inference__(preprocessed)

    def __preprocess__(self, img_arr):
        pass

    def __inference__(self, img_arr_preprocessed):
        pass

import io
import os
from pathlib import Path
from PIL import Image
import json

import torchvision.transforms as transforms
import torch
from config import ModelsConfig

class ClassifyOptions:
    def __init__(self) -> None:
        self.CLASSIFIER_MODEL = ModelsConfig.ClassifierConfig.MODEL_FILE

class ClassifierPrediction:
    def __init__(self, class_percents:dict) -> None:
        self.type = None
        self.categories = {}
        if class_percents:
            for class_, percent in class_percents.items():
                type_, class_name = class_.split('_', 1)
                if not self.type:
                    self.type = type_
                self.categories[class_name.lower()] = percent
    
    def serialize(self) -> dict:
        return {
            'type': self.type,
            'categories': self.categories
        }

class TeaLeafClassifier:
    CLASS_NAMES = [
        "Fresh_Below_Best",
        "Fresh_Best",
        "Fresh_Poor",
        "Withered_Below_Best",
        "Withered_Best",
        "Withered_Poor",
    ]

    def __init__(self) -> None:
        self.img_transforms = transforms.Compose(
            [
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )
        self.options = ClassifyOptions()

    def predict(self, img_path):
        tensor = None
        with open(img_path, "rb") as f:
            image_bytes = f.read()
            tensor = self.__transform_image__(image_bytes=image_bytes)
            # print(tensor)
        return self.__predict__(tensor)

    def __get_device__(self):
        return torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    def __transform_image__(self, image_bytes):
        image = Image.open(io.BytesIO(image_bytes))
        return self.img_transforms(image).unsqueeze(0)

    def __predict__(self, img_tensor):
        if img_tensor is None:
            raise Exception("Image tensor cannot be None.")
        device = self.__get_device__()
        model = torch.load(self.options.CLASSIFIER_MODEL, map_location=device)
        img_tensor = img_tensor.to(device)
        output = model(img_tensor)
        _, pred = torch.max(output, 1)
        return self.CLASS_NAMES[pred]

class TeaLeavesClassifier:
    def __init__(self, dir_path:Path, classifier:TeaLeafClassifier = None) -> None:
        self.img_paths = [os.path.join(dir_path, filename) for filename in os.listdir(dir_path)]
        self.total_images = len(self.img_paths)
        self.classifier = classifier if classifier else TeaLeafClassifier()
    
    def predictions(self) -> ClassifierPrediction:
        classes_dict = {}
        for img_path in self.img_paths:
            prediction = self.classifier.predict(img_path)
            
            if prediction not in classes_dict:
                classes_dict[prediction] = []
            classes_dict[prediction].append(img_path)
        
        class_percents = {k : 100 * len(v) / self.total_images for k, v in classes_dict.items()}
        return ClassifierPrediction(class_percents)

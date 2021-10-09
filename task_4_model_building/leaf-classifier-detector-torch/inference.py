# Usage:
# $ python3 inference.py -i example-images/Low_Fresh_Poor_36.jpg

import io
import argparse
from PIL import Image

import torchvision.transforms as transforms
import torch

TEST_FILE_PATH = "example-images/Low_Fresh_Below_best_36.jpg"
MODEL_FILE_PATH = "model_resnet_18.pth"
CLASS_NAMES = [
    "Fresh_Below_Best",
    "Fresh_Best",
    "Fresh_Poor",
    "Withered_Below_Best",
    "Withered_Best",
    "Withered_Poor",
]


def get_device():
    return torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def transform_image(image_bytes):
    img_transforms = transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    image = Image.open(io.BytesIO(image_bytes))
    return img_transforms(image).unsqueeze(0)


def predict(device, img_tensor):
    model = torch.load("model_resnet_18.pth", map_location=device)
    img_tensor = img_tensor.to(device)
    output = model(img_tensor)
    _, pred = torch.max(output, 1)
    return CLASS_NAMES[pred]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--img_path", "-i", type=str, required=True, help="Path of the image file"
    )
    args = ap.parse_args()

    tensor = None
    with open(args.img_path, "rb") as f:
        image_bytes = f.read()
        tensor = transform_image(image_bytes=image_bytes)
        # print(tensor)
    device = get_device()
    print(device)
    prediction = predict(device, tensor)
    print(prediction)

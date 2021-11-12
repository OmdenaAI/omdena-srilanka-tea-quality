'''
Usage:
python3 model_main.py \
  --img-path '../assets/samples/Low_Withered_Best.jpg'
'''
import argparse

from detect import Detector
from classify import TeaLeavesClassifier
import logging

logging.basicConfig(
    filename='../outputs/logs/model_main.log',
    filemode='a',
    level=logging.DEBUG)

def run_pipeline(img_path):
    logger = logging.getLogger()
    detector = Detector(logger, img_path)
    # This model will save detected tea leaves in the image into individual files.
    exp_detected_dir = detector.detect()

    classifier = TeaLeavesClassifier(exp_detected_dir)
    predictions = classifier.predictions()
    print("=== PREDICTIONS ===")
    print(predictions.serialize())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--img-path", "-i", type=str, required=True, help="Path of the image file"
    )
    opt = parser.parse_args()
    # print(opt)

    run_pipeline(opt.img_path)

import argparse
import torch
import os
import torchvision.transforms as transforms
from pathlib import Path

from detect import detect
from classify import transform_image, predict

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--weights", nargs="+", type=str, default="yolov5s.pt", help="model.pt path(s)"
    )
    parser.add_argument(
        "--source", type=str, default="data/images", help="source"
    )  # file/folder, 0 for webcam
    parser.add_argument(
        "--img-size", type=int, default=640, help="inference size (pixels)"
    )
    parser.add_argument(
        "--conf-thres", type=float, default=0.25, help="object confidence threshold"
    )
    parser.add_argument(
        "--iou-thres", type=float, default=0.45, help="IOU threshold for NMS"
    )
    parser.add_argument(
        "--device", default="", help="cuda device, i.e. 0 or 0,1,2,3 or cpu"
    )
    parser.add_argument("--view-img", action="store_true", help="display results")
    parser.add_argument("--save-txt", action="store_true", help="save results to *.txt")
    parser.add_argument(
        "--save-conf", action="store_true", help="save confidences in --save-txt labels"
    )
    parser.add_argument(
        "--classes",
        nargs="+",
        type=int,
        help="filter by class: --class 0, or --class 0 2 3",
    )
    parser.add_argument(
        "--agnostic-nms", action="store_true", help="class-agnostic NMS"
    )
    parser.add_argument("--augment", action="store_true", help="augmented inference")
    parser.add_argument("--update", action="store_true", help="update all models")
    parser.add_argument(
        "--project", default="outputs/detect", help="save results to project/name"
    )
    parser.add_argument("--name", default="exp", help="save results to project/name")
    parser.add_argument(
        "--exist-ok",
        action="store_true",
        help="existing project/name ok, do not increment",
    )
    parser.add_argument(
        "--img-path", "-i", type=str, required=True, help="Path of the image file"
    )
    parser.add_argument(
        "--classify-model", "-cm", type=str, required=True, help="Classifier model path"
    )
    opt = parser.parse_args()
    print(opt)

    with torch.no_grad():
        # This model will save detected tea leaves in the image into individual files.
        exp_detected_dir = detect(opt, save_img=True)

        print(exp_detected_dir)

        imgs = os.listdir(exp_detected_dir)
        classes_dict = {}
        for det_file in imgs:
            det_file_path = os.path.join(exp_detected_dir, det_file)
            tensor = None
            with open(det_file_path, "rb") as f:
                image_bytes = f.read()
                tensor = transform_image(image_bytes=image_bytes)
                # print(tensor)
            prediction = predict(tensor, opt.classify_model)
            if prediction not in classes_dict:
                classes_dict[prediction] = []
            classes_dict[prediction].append(det_file)
        # print(classes_dict)
        total_det_imgs = len(imgs)
        class_percents = {k:100*len(v)/total_det_imgs for k,v in classes_dict.items()}
        print(class_percents)

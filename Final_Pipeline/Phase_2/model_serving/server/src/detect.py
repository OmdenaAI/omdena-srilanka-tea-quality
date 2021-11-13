import argparse
import time
from pathlib import Path
import os

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import (
    check_img_size,
    non_max_suppression,
    apply_classifier,
    scale_coords,
    xyxy2xywh,
    strip_optimizer,
    set_logging,
    increment_path,
)
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized
from config import ModelsConfig
import json

class DetectOptions:
    def __init__(self, img_path) -> None:
        self.source = img_path
        self.agnostic_nms = ModelsConfig.DetectorConfig.AGNOSTIC_NMS
        self.augment = ModelsConfig.DetectorConfig.AUGMENT
        self.classes = ModelsConfig.DetectorConfig.CLASSES
        self.conf_thres = ModelsConfig.DetectorConfig.CONF_THRES
        self.device = ModelsConfig.DetectorConfig.DEVICE
        self.exist_ok = ModelsConfig.DetectorConfig.EXIST_OK
        self.img_size = ModelsConfig.DetectorConfig.IMG_SIZE
        self.iou_thres = ModelsConfig.DetectorConfig.IOU_THRESH
        self.name = ModelsConfig.DetectorConfig.NAME
        self.project = ModelsConfig.DetectorConfig.PROJECT
        self.save_conf = ModelsConfig.DetectorConfig.SAVE_CONF
        self.save_txt = ModelsConfig.DetectorConfig.SAVE_TXT
        self.update = ModelsConfig.DetectorConfig.UPDATE
        self.view_img = ModelsConfig.DetectorConfig.VIEW_IMG
        self.weights = ModelsConfig.DetectorConfig.WEIGHTS_FILE
        self.detected = ModelsConfig.DetectorConfig.DETECTED_NAME
    
    def __str__(self) -> str:
        return json.dumps(self.__dict__)

class Detector:
    def __init__(self, logger, file_path:str = None, options:DetectOptions = None) -> None:
        self.logger = logger
        if not options:
            assert file_path != ''
            assert os.path.exists(file_path)
        self.options = options if options else DetectOptions(file_path)

    def detect(self) -> Path:
        with torch.no_grad():
            return self.__detect_internal__()

    def __detect_internal__(self, save_img=True):
        source, weights, view_img, save_txt, imgsz = (
            self.options.source,
            self.options.weights,
            self.options.view_img,
            self.options.save_txt,
            self.options.img_size,
        )

        webcam = False
        # webcam = (
        #     source.isnumeric()
        #     or source.endswith(".txt")
        #     or source.lower().startswith(("rtsp://", "rtmp://", "http://"))
        # )

        # Directories
        save_dir = Path(
            increment_path(Path(self.options.project) / self.options.name,
            exist_ok=self.options.exist_ok)
        )  # increment run
        save_detected_dir = save_dir / self.options.detected
        save_detected_dir.mkdir(parents=True, exist_ok=True)  # make dir

        # Initialize
        # set_logging()
        device = select_device(self.options.device)
        self.logger.debug(f"Device={device}")
        half = device.type != "cpu"  # half precision only supported on CUDA

        # Load model
        model = attempt_load(weights, map_location=device)  # load FP32 model
        imgsz = check_img_size(imgsz, s=model.stride.max())  # check img_size
        if half:
            model.half()  # to FP16

        # # Second-stage classifier
        # classify = False
        # if classify:
        #     modelc = load_classifier(name="resnet101", n=2)  # initialize
        #     modelc.load_state_dict(
        #         torch.load("weights/resnet101.pt", map_location=device)["model"]
        #     ).to(device).eval()

        # Set Dataloader
        save_img = True
        dataset = LoadImages(source, img_size=imgsz)
        # vid_path, vid_writer = None, None
        # if webcam:
        #     view_img = True
        #     cudnn.benchmark = True  # set True to speed up constant image size inference
        #     dataset = LoadStreams(source, img_size=imgsz)
        # else:
        #     save_img = True
        #     dataset = LoadImages(source, img_size=imgsz)


        # Get names and colors
        names = model.module.names if hasattr(model, "module") else model.names
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

        # Run inference
        t0 = time.time()
        img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
        _ = model(img.half() if half else img) if device.type != "cpu" else None  # run once
        for path, img, im0s, vid_cap in dataset:
            img_ext = path.split(".")[-1]
            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Inference
            t1 = time_synchronized()
            pred = model(img, augment=self.options.augment)[0]

            # Apply NMS
            pred = non_max_suppression(
                pred,
                self.options.conf_thres,
                self.options.iou_thres,
                classes=self.options.classes,
                agnostic=self.options.agnostic_nms,
            )
            t2 = time_synchronized()

            # # Apply Classifier
            # if classify:
            #     pred = apply_classifier(pred, modelc, img, im0s)

            # Process detections
            for i, det in enumerate(pred):  # detections per image
                if webcam:  # batch_size >= 1
                    p, s, im0 = Path(path[i]), "%g: " % i, im0s[i].copy()
                else:
                    p, s, im0 = Path(path), "", im0s

                save_path = str(save_dir / p.name)
                s += "%gx%g " % img.shape[2:]  # print string
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += "%g %ss, " % (n, names[int(c)])  # add to string

                    # Write results
                    counter = 0
                    for *xyxy, conf, cls in reversed(det):
                        xywh = (
                            (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn)
                            .view(-1)
                            .tolist()
                        )  # normalized xywh
                        line = (
                            (cls, *xywh, conf) if self.options.save_conf else (cls, *xywh)
                        )  # label format

                        # Crop a xywh subimage in the top left corner
                        c1, c2 = (int(xyxy[0]), int(xyxy[1])), (
                            int(xyxy[2]),
                            int(xyxy[3]),
                        )
                        raw_img = cv2.imread(path)
                        # raw_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2RGB)
                        cropped_image = raw_img[c1[1] : c2[1], c1[0] : c2[0]]
                        # print(i)
                        cv2.imwrite(
                            str(save_detected_dir / f"det_{counter}.{img_ext}"),
                            cropped_image,
                        )
                        counter = counter + 1

                        if save_img or view_img:  # Add bbox to image
                            label = "%s %.2f" % (names[int(cls)], conf)
                            plot_one_box(
                                xyxy,
                                im0,
                                label=label,
                                color=colors[int(cls)],
                                line_thickness=3,
                            )

                # Print time (inference + NMS)
                self.logger.info("%sDone. (%.3fs)" % (s, t2 - t1))

                # Stream results
                if view_img:
                    cv2.imshow(str(p), im0)
                    if cv2.waitKey(1) == ord("q"):  # q to quit
                        raise StopIteration

                # Save results (image with detections)
                if save_img:
                    if dataset.mode == "images":
                        cv2.imwrite(save_path, im0)
                    else:
                        if vid_path != save_path:  # new video
                            vid_path = save_path
                            if isinstance(vid_writer, cv2.VideoWriter):
                                vid_writer.release()  # release previous video writer

                            fourcc = "mp4v"  # output video codec
                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                            vid_writer = cv2.VideoWriter(
                                save_path, cv2.VideoWriter_fourcc(*fourcc), fps, (w, h)
                            )
                        vid_writer.write(im0)

        if save_txt or save_img:
            s = (
                f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}"
                if save_txt
                else ""
            )
            self.logger.info(f"Results saved to {save_dir}{s}")

        self.logger.info("Done. (%.3fs)" % (time.time() - t0))

        return save_detected_dir

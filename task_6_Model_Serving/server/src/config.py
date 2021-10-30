class ModelsConfig:
    class DetectorConfig:
        WEIGHTS_FILE = 'assets/detector-weights-file/tea_leaves.pt'
        PROJECT = 'outputs/detect'
        NAME = 'exp'
        DETECTED_NAME = 'detected'
        DEVICE = ''
        CLASSES = None
        
        IMG_SIZE = 640
        CONF_THRES = 0.25
        IOU_THRESH = 0.45
        
        EXIST_OK = True
        VIEW_IMG = False
        SAVE_TXT = False
        SAVE_CONF = False
        AUGMENT = False
        UPDATE = False
        AGNOSTIC_NMS = False

    
    class ClassifierConfig:
        MODEL_FILE = 'assets/classifier-model-file/model_resnet_18.pth'
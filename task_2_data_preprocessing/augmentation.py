import os
import numpy as np
import cv2
import albumentations as A
from tqdm import tqdm



def augment_every_image(images, save_path='./augmented_images', resize_shape=None, seed=43,
                        horizontal_flip=True, vertical_flip=True, elastic_transform=False, grid_distortion=True,
                        optical_distortion=True, random_brightness_contrast=True, random_gamma=True, iso_noise=True, clahe=True,
                        random_rotate_90=True, transpose=True, blur=True, flip=True, equalize=False):
    
    """ 
    Performs augmentation techniques (for every augmentation technique set to true) on every image in the given path, and stores them in the specified folder, 
    and also reshapes the data given the specified shape.
    
    #Parameters:
        images: Takes a variable containing a list the paths to the images to be augmented on. Must be a list!
        save_path: Where the preprocessed images will be stored. If path does not exist, it is created
        resize_shape: Reshapes the orignal images and augmented images based on the given size (Height, Width)
    
    """
    np.random.seed(seed)
    
    """creates a path if it doesn't exist"""
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print("{} created.".format(save_path))
    
    for i, x in tqdm(enumerate(images), total=len(images)):
        
        X = []

        
        # Extract name to save in the augment folder
        name = x.split('/')[-1].split('.')[0]
        
        # Reading image and mask
        x = cv2.imread(x, cv2.IMREAD_COLOR)
        X.append(x)

        if horizontal_flip:
            aug = A.HorizontalFlip(p=1.0)
            augmented = aug(image=x)
            X.append(augmented['image'])
        
        if vertical_flip:
            aug = A.VerticalFlip(p=1.0)
            augmented = aug(image=x)
            X.append(augmented['image'])
        
        if elastic_transform:
            aug = A.ElasticTransform(p=1, alpha=0.34, sigma=120*0.05, alpha_affine=68.46)
            augmented = aug(image=x)
            X.append(augmented['image'])

        if grid_distortion:
            aug = A.GridDistortion(p=1)
            augmented = aug(image=x)
            X.append(augmented['image'])
        
        if optical_distortion:
            aug = A.OpticalDistortion(p=1, distort_limit=2, shift_limit=0.5)
            augmented = aug(image=x)
            X.append(augmented['image'])
        
        if random_brightness_contrast:        
            aug = A.RandomBrightnessContrast(p=1, brightness_limit=[-0.06, 0.24], contrast_limit=[-0.21, 0.45])
            augmented = aug(image=x)
            X.append(augmented['image'])
        
        if random_gamma:
            aug = A.RandomGamma(p=1, gamma_limit=[80, 150])
            augmented = aug(image=x)
            X.append(augmented['image'])
        
        if iso_noise:
            aug = A.ISONoise(p=1, intensity=[0.36, 1])
            augmented = aug(image=x)
            X.append(augmented['image'])
        
        if clahe:
            aug = A.CLAHE()
            augmented = aug(image=x)
            X.append(augmented['image'])
        
        if random_rotate_90:
            aug = A.RandomRotate90(p=1)
            augmented = aug(image=x)
            X.append(augmented['image'])
        
        if transpose:
            aug = A.Transpose(p=1)
            augmented = aug(image=x)
            X.append(augmented['image'])
        
        if blur:
            aug = A.Blur(p=1, blur_limit=[3, 6])
            augmented = aug(image=x)
            X.append(augmented['image'])
        
        if flip:
            aug = A.Flip(p=1)
            augmented = aug(image=x)
            X.append(augmented['image'])
            
        if equalize:
            aug = A.Equalize(p=1)
            augmented = aug(image=x)
            X.append(augmented['image'])


        
        
            
        index = 0
        for image in X:
            
            if resize_shape:     
                H, W = resize_shape 
                image = cv2.resize(image, (W, H))
            
            if len(X) == 1:
                tmp_image_name = f"{name}.jpg"
            else:
                tmp_image_name = f"{name}_{index}.jpg"
            
            image_path = os.path.join(save_path, tmp_image_name)
        
            cv2.imwrite(image_path, image)

            index += 1
            
        
    return 'Done!'




def multiple_augmentations_on_an_image(images, save_path='./augmented_images', resize_shape=None, seed=43):
    """ 
    Performs a combined variation of augmentation techniques on every image in the given list of paths, and stores them in the specified folder, 
    It also reshapes the images if a specific shape is given.
    
    #Parameters:
        images: Takes a variable containing a list the paths to the images to be augmented on. Must be a list!
        save_path: Where the preprocessed images will be stored. If path does not exist, it is created
        resize_shape: Reshapes the orignal images and augmented images based on the given size (Height, Width)
    
    """
    np.random.seed(seed)
    
    """ Creates a path if it doesn't exist. """
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print("{} created.".format(save_path))
    
    """ Pipelines of transformations """
    transform_1 = A.Compose([
        A.CLAHE(),
        A.RandomRotate90(),
        A.Transpose(),
        A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.50, rotate_limit=45, p=.75),
        A.Blur(blur_limit=3),
        A.OpticalDistortion(),
        A.GridDistortion(),
        A.HueSaturationValue(),
        ])
    
    
    transform_2 = A.Compose([
        A.RandomRotate90(),
        A.Flip(),
        A.Transpose(),
        A.GaussNoise(p=0.2),
        A.OneOf([
            A.MotionBlur(p=.2),
            A.MedianBlur(blur_limit=3, p=0.1),
            A.Blur(blur_limit=3, p=0.1),
        ], p=0.2),
        A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.2, rotate_limit=45, p=0.2),
        A.OneOf([
            A.OpticalDistortion(p=0.3),
            A.GridDistortion(p=.1),
            A.PiecewiseAffine(p=0.3),
        ], p=0.2),
        A.OneOf([
            A.CLAHE(clip_limit=2),
            A.Sharpen(),
            A.Emboss(),
            A.RandomBrightnessContrast(),            
        ], p=0.3),
        A.HueSaturationValue(p=0.3),
        ])
    
    transform_3 = A.Compose([
        A.RandomRotate90(),
        A.Flip(),
        A.Transpose(),
        A.OneOf([
            A.MotionBlur(p=.2),
            A.MedianBlur(blur_limit=3, p=0.3),
            A.Blur(blur_limit=3, p=0.1),
        ], p=0.2),
        A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.2, rotate_limit=45, p=0.2),
        A.OneOf([
            A.OpticalDistortion(p=0.3),
            A.GridDistortion(p=.1),
        ], p=0.2),
        A.OneOf([
            A.CLAHE(clip_limit=2),
            A.RandomBrightnessContrast(),            
        ], p=0.3),
        A.HueSaturationValue(p=0.3),
        ])
    
    transform_4 = A.Compose([
        A.CLAHE(),
        A.RandomRotate90(),
        A.Transpose(),
        A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.50, rotate_limit=45, p=.75),
        A.Blur(blur_limit=3),
        A.OpticalDistortion(),
        ])
    
    transform_5 = A.Compose([
        A.Transpose(p=0.5),
        A.Flip(p=0.5),
        A.OneOf([
            A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.3),
            A.RandomBrightnessContrast(brightness_limit=0.1, contrast_limit=0.1)
            ],p=1),
        A.GaussianBlur(p=0.05),
        A.HueSaturationValue(p=0.5),
        A.RGBShift(p=0.5),
        ])

    
    
    """ Reads every image from the given paths, performs transformations and saves the newly created image. """
    for i, x in tqdm(enumerate(images), total=len(images)):
        
        X = []
        
        # Extract name to save in the augment folder
        name = x.split('/')[-1].split('.')[0]
        
        # Reading image and mask
        x = cv2.imread(x, cv2.IMREAD_COLOR)
        X.append(x)
        
        
        augmented = transform_1(image=x)
        X.append(augmented['image'])

        augmented = transform_2(image=x)
        X.append(augmented['image'])
        
        augmented = transform_3(image=x)
        X.append(augmented['image'])
        
        augmented = transform_4(image=x)
        X.append(augmented['image'])
        
        augmented = transform_5(image=x)
        X.append(augmented['image'])

            
        index = 0
        for image in X:
            
            if resize_shape:     
                H, W = resize_shape 
                image = cv2.resize(image, (W, H))
            
            if len(X) == 1:
                tmp_image_name = f"{name}.jpg"
            else:
                tmp_image_name = f"{name}_{index}.jpg"
            
            image_path = os.path.join(save_path, tmp_image_name)
        
            cv2.imwrite(image_path, image)

            index += 1
            
    return 'Done!'
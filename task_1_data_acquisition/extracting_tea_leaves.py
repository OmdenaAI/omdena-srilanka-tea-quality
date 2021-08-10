
import cv2
import numpy as np
from google.colab import files
# To upload pictures manually to google collab
![pic](https://drive.google.com/file/d/1Y_VW7t-BLyXVA98uXwzJlis8v2Z9Njwq/view?usp=sharing)

# select the required pictures and upload
uploaded = files.upload()


img = cv2.imread('IMG_2663.jpg')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

mask = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))

# Extracting green color present in the image
imask = mask>0
green = np.zeros_like(img, np.uint8)
green[imask] = img[imask]

# Save the image with the respected name
cv2.imwrite("green_multi.png", green)




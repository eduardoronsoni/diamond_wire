import numpy as np
import cv2
import os
import matplotlib.pyplot as plt

path = "D:\diamond_wire\images\Fio_2.1.tif"
image_path = "D:\diamond_wire\images"
imgBig = cv2.imread(path,0)

scale_percent = 50 # percent of original size
w = int(imgBig.shape[1] * scale_percent / 100)
h = int(imgBig.shape[0] * scale_percent / 100)
dim = (w, h)

# resize image
img = cv2.resize(imgBig, dim, interpolation=cv2.INTER_AREA)


#binarizing image

_, binary = cv2.threshold(img, 90, 255, cv2.THRESH_BINARY)

cv2.imshow('Binary', binary)
cv2.imwrite(os.path.join(image_path, 'mask_2.1.tif'), binary)
cv2.waitKey(0)
cv2.destroyAllWindows()
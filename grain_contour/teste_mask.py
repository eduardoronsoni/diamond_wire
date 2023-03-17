import numpy as np
import cv2

imgBig = cv2.imread('fio_2.8.tif')

scale_percent = 100  # percent of original size
w = int(imgBig.shape[1] * scale_percent / 100)
h = int(imgBig.shape[0] * scale_percent / 100)
dim = (w, h)

# Masking Image
imgResized = cv2.resize(imgBig, dim, interpolation=cv2.INTER_AREA)
mask = ask = cv2.imread('mask_2.8.tif')
img = cv2.bitwise_and(imgResized, mask)

#





cv2.imshow('Masked Image', img)
cv2.waitKey(0)
cv2.






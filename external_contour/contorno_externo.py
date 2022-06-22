#passo a passo:
#binarize (thresh =109 ~ 111)  - despeckle

import numpy as np
import cv2
import matplotlib.pyplot as plt


imgBig = cv2.imread('fio_2.1.tif',0)

scale_percent = 80 # percent of original size
w = int(imgBig.shape[1] * scale_percent / 100)
h = int(imgBig.shape[0] * scale_percent / 100)
dim = (w, h)

# resize image
imgResized = cv2.resize(imgBig, dim, interpolation=cv2.INTER_AREA)
#
# crop image
y = 0
x = 0
img = imgResized[(y):(h-y-70),x:w]
img_copy = img.copy()
print(img.shape)


#binarizing image

_, binary = cv2.threshold(img, 112, 255, cv2.THRESH_BINARY)


#Noise reduction - Bilateral blur
bilateral = cv2.bilateralFilter(binary, 5, 75, 75)

#Finding Contours - Método certo - Tentar implementar autotresholding pra ficar generalizado
#contours, hierarchy = cv2.findContours(bilateral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#cv2.drawContours(img_copy,contours, -1, (0, 255, 0), 3)


#Tentaiva de contour
contours, hierarchy = cv2.findContours(bilateral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
largest_contours = sorted(contours, key=cv2.contourArea)[-1:]
cv2.drawContours(img_copy, largest_contours, -1, (0, 255, 0), 2)




#showing images

cv2.imshow('Cropped Image', img)
cv2.imshow('Bilateral Image', bilateral)
cv2.imshow('Contours Image', img_copy)
cv2.waitKey(0)
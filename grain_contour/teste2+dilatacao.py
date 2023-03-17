import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.filters import sobel
import scipy.ndimage as ndimage
import skimage.exposure as exposure

imgBig = cv2.imread('fio_2.8.tif',0)

scale_percent = 100 # percent of original size
w = int(imgBig.shape[1] * scale_percent / 100)
h = int(imgBig.shape[0] * scale_percent / 100)
dim = (w, h)

# resize image
# imgResized = cv2.resize(imgBig, dim, interpolation=cv2.INTER_AREA)
#
# # crop image
# y = 460
# x = 0
# img = imgResized[(y):(h-y-70),x:w]
# img_copy = img.copy()
# print(img.shape)
img = cv2.resize(imgBig, dim, interpolation=cv2.INTER_AREA)
img_copy = img.copy()
img_copy2 = img.copy()
#Histogram equalization - CLAHE - Contrast Limited Adaptive Histogram Equalization
clahe = cv2.createCLAHE(clipLimit = 2.0, tileGridSize=(8,8))
cl_img = clahe.apply(img)

#Noise reduction - Bilateral blur
bilateral = cv2.bilateralFilter(cl_img, 5, 75, 75)

#Image Sharpening using Sobel Filter
#sobel_img = sobel(bilateral)
# print(sobel_img.dtype)
#sobel_img = cv2.Sobel(src=bilateral, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=3)
# cv2.convertScaleAbs(sobel_img)

# apply sobel derivatives
sobelx = cv2.Sobel(bilateral,cv2.CV_64F,1,0,ksize=3)
sobely = cv2.Sobel(bilateral,cv2.CV_64F,0,1,ksize=3)

# optionally normalize to range 0 to 255 for proper display
sobelx_norm= exposure.rescale_intensity(sobelx, in_range='image', out_range=(0,255)).clip(0,255).astype(np.uint8)
sobely_norm= exposure.rescale_intensity(sobelx, in_range='image', out_range=(0,255)).clip(0,255).astype(np.uint8)

# square
sobelx2 = cv2.multiply(sobelx,sobelx)
sobely2 = cv2.multiply(sobely,sobely)

# add together and take square root
sobel_magnitude = cv2.sqrt(sobelx2 + sobely2)

# normalize to range 0 to 255 and clip negatives
sobel_magnitude = exposure.rescale_intensity(sobel_magnitude, in_range='image', out_range=(0,255)).clip(0,255).astype(np.uint8)


# Trying Canny
canny = cv2.Canny(bilateral, 50, 150)
print(canny.shape)

#Morphological process - Opening
kernel = np.ones((3,3),np.uint8)
dilation = cv2.dilate(canny, kernel, iterations = 1)
print(dilation.shape)



#Finding Contours
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
largest_contours = sorted(contours, key=cv2.contourArea)[-20:]
cv2.drawContours(img_copy, largest_contours, -1, (0, 255, 0), -1)

closed_contours = []

for cnt in contours:
   if cv2.isContourConvex(cnt) == True:
      closed_contours.append(cnt)
   else:
      pass
print(closed_contours)
sorted_close = sorted(closed_contours, key=cv2.contourArea)
cv2.drawContours(img_copy2, sorted_close, -1, (0, 255, 0), -1)



#Displaying the images
#cv2.imshow('CLAHE Image', cl_img)
#cv2.imshow('Bilateral Filter', bilateral)
# plot = np.concatenate((bilateral, bilateral2, bilateral3, bilateral4, bilateral5,bilateral6,bilateral7), axis = 0)
# cv2.imshow('Plot', plot)
cv2.imshow('Bilateral', bilateral)
cv2.imshow('Canny', canny)
cv2.imshow('Dilation after Canny', dilation)
# cv2.imshow('Opened Sobel', opening)
cv2.imshow('Contours', img_copy)
cv2.imshow('Closed Contours', img_copy2)

cv2.waitKey(0)
cv2.destroyAllWindows()
import numpy as np
import cv2

imgBig = cv2.imread('fio_2.1.tif',0)

scale_percent = 50  # percent of original size
w = int(imgBig.shape[1] * scale_percent / 100)
h = int(imgBig.shape[0] * scale_percent / 100)
dim = (w, h)

# resize image
imgResized = cv2.resize(imgBig, dim, interpolation=cv2.INTER_AREA)

# crop image
y = 60
x = 0
img = imgResized[(y):(h-y),x:w]
img_copy = img.copy()


median_blur = cv2.medianBlur(img, 3)
#combinações testadas(55,94) (110,212)(160,212)(90,211)
edges = cv2.Canny(median_blur, 90, 212)

kernel = np.ones((3,3), np.uint8)/9

dilation = cv2.dilate(edges, kernel, iterations = 1)
#erosion = cv2.erode(dilation, kernel, iterations = 1)


contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img_copy, contours, -1, (0,255,0), 3)

biggest_contour = max(contours, key = cv2.contourArea)
img_copy2 = img.copy()
cv2.drawContours(img_copy2, biggest_contour, -1, (0,255,0), 4)



print("Number of Contours found = " + str(len(contours)))


cv2.imshow('Original', img)
cv2.imshow('Median Blur', median_blur)
cv2.imshow('Dilation', dilation)
# cv2.imshow('Erosion', erosion)
cv2.imshow('Canny Edge Detection', edges)
cv2.imshow('Contours', img_copy)
cv2.imshow('Biggest', img_copy2)
cv2.waitKey(0)
cv2.destroyAllWindows()
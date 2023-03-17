import cv2
import numpy as np
import matplotlib.pyplot as plt

def callback(x):
    print(x)

path = "D:\diamond_wire\images\fio_2.8.tif"
imgBig = cv2.imread(path, 0)

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

median_blur = cv2.medianBlur(img, 3)

clahe = cv2.createCLAHE(clipLimit = 2.0, tileGridSize=(8,8))
cl_img = clahe.apply(img)

#Noise reduction - Bilateral blur
bilateral = cv2.bilateralFilter(cl_img, 5, 75, 75)

canny = cv2.Canny(bilateral, 85, 255)


cv2.namedWindow('image') # make a window with name 'image'
cv2.createTrackbar('L', 'image', 0, 255, callback) #lower threshold trackbar for window 'image
cv2.createTrackbar('U', 'image', 0, 255, callback) #upper threshold trackbar for window 'image

while(1):
    numpy_horizontal_concat = np.concatenate((median_blur, canny), axis=1) # to display image side by side
    cv2.imshow('image', numpy_horizontal_concat)
    k = cv2.waitKey(1) & 0xFF
    if k == 27: #escape key
        break
    l = cv2.getTrackbarPos('L', 'image')
    u = cv2.getTrackbarPos('U', 'image')

    canny = cv2.Canny(median_blur, l, u)

cv2.destroyAllWindows()
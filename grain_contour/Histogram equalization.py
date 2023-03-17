import numpy as np
import cv2
import matplotlib.pyplot as plt

imgBig = cv2.imread('fio_2.8.tif', 0)

scale_percent = 100 # percent of original size
w = int(imgBig.shape[1] * scale_percent / 100)
h = int(imgBig.shape[0] * scale_percent / 100)
dim = (w, h)

# resize image
imgResized = cv2.resize(imgBig, dim, interpolation=cv2.INTER_AREA)

# crop image
# y = 460
# x = 0
# img = imgResized[(y):(h-y-70),x:w]
# img_copy = img.copy()
# print(img.shape)
imgTest = imgResized

eq_img = cv2.equalizeHist(imgTest)

plt.hist(eq_img.flat, bins = 100, range =(0,255))
plt.show()

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl_img = clahe.apply(imgTest)

median_blur = cv2.medianBlur(cl_img, 3)

canny = cv2.Canny(median_blur, 85, 255)
def callback(x):
    print(x)


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


ret,thresh = cv2.threshold(median_blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)


contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
# Draw all the contours.
contour_image = cv2.drawContours(imgTest, contours, -1, (0,255,0), 3)

edges = cv2.Canny(median_blur, 80, 150)

# Blurring to filter noise

cv2.imshow('Canny Edge Detection', edges)
cv2.imshow('Contours', contour_image)
cv2.imshow('Equalized Image', eq_img)
cv2.imshow('CLAHE Image', cl_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
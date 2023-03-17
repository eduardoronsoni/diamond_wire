import numpy as np
import cv2
import matplotlib.pyplot as plt

imgBig = cv2.imread('fio_2.8.tif')

scale_percent = 100 # percent of original size
w = int(imgBig.shape[1] * scale_percent / 100)
h = int(imgBig.shape[0] * scale_percent / 100)
dim = (w, h)

# resize image
imgResized = cv2.resize(imgBig, dim, interpolation=cv2.INTER_AREA)

# crop image
y = 460
x = 0
img = imgResized[(y):(h-y-70),x:w]
img_copy = img.copy()
print(img.shape)


#converting to grayscale
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(imgGray.shape)

hist = cv2.calcHist([imgGray], [0], None, [256], [0,256] )
plt.hist(imgGray.ravel(),256,[0,256]);
plt.show()


median_blur = cv2.medianBlur(imgGray, 3)


kernel_sharpen_1 = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
kernel_sharpen_2 = np.array([[1,1,1], [1,-7,1], [1,1,1]])
kernel_sharpen_3 = np.array([[-1,-1,-1,-1,-1],
[-1,2,2,2,-1],
[-1,2,8,2,-1],
[-1,2,2,2,-1],
[-1,-1,-1,-1,-1]]) / 8.0
# applying different kernels to the input image
output_1 = cv2.filter2D(median_blur, -1, kernel_sharpen_1)
output_2 = cv2.filter2D(median_blur, -1, kernel_sharpen_2)
output_3 = cv2.filter2D(median_blur, -1, kernel_sharpen_3)
cv2.imshow('Sharpening', output_1)
cv2.imshow('Excessive Sharpening', output_2)
cv2.imshow('Edge Enhancement', output_3)
cv2.waitKey(0)
cv2.destroyAllWindows()
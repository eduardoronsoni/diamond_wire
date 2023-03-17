import numpy as np
import cv2
import matplotlib.pyplot as plt


path = "D:\diamond_wire\images\Fio_2.8.tif"
imgBig = cv2.imread('path')

# scale_percent = 100 # percent of original size
# w = int(imgBig.shape[1] * scale_percent / 100)
# h = int(imgBig.shape[0] * scale_percent / 100)
# dim = (w, h)

# resize image
# imgResized = cv2.resize(imgBig, dim, interpolation=cv2.INTER_AREA)

# # crop image
# y = 460
# x = 0
# img = imgResized[(y):(h-y-70),x:w]
# img_copy = img.copy()
# print(img.shape)


#converting to grayscale
imgGray = cv2.cvtColor(imgBig, cv2.COLOR_BGR2GRAY)
print(imgGray.shape)

hist = cv2.calcHist([imgGray], [0], None, [256], [0,256] )
plt.hist(imgGray.ravel(),256,[0,256])
plt.show()


median_blur = cv2.medianBlur(imgGray, 3)

kernel_sharpen_1 = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
kernel_sharpen_2 = np.array([[1,1,1], [1,-7,1], [1,1,1]])
kernel_sharpen_3 = np.array([[-1,-1,-1,-1,-1],
[-1,2,2,2,-1],
[-1,2,8,2,-1],
[-1,2,2,2,-1],
[-1,-1,-1,-1,-1]]) / 8.0
output_1 = cv2.filter2D(median_blur, -1, kernel_sharpen_1)
output_3 = cv2.filter2D(median_blur, -1, kernel_sharpen_3)


median_blur2 =  cv2.medianBlur(output_3, 3)
#
ret,thresh = cv2.threshold(median_blur2,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
# Draw all the contours.
contour_image = cv2.drawContours(img_copy, contours, -1, (0,255,0), 3)

# # Loop over all the contours detected
# for i,cont in enumerate(contours):
# # If the contour is at first level draw it in green
#     if hierarchy[0][i][3] == -1:
#         img_copy = cv2.drawContours(img_copy, cont, -1, (0,255,0), 3)
# # else draw the contour in Red
#     else:
#         img_copy = cv2.drawContours(img_copy, cont, -1, (255,0,0), 3)
# # # Print the number of Contours returned
# # print("Number of Contours Returned: {}".format(len(contours)))
# #



##### fazer dilation e erosion antes de tirar o contorno
cv2.imshow('Original Image', img)
cv2.imshow('Thresholded Image', thresh)
plot = np.concatenate((imgGray, thresh), axis = 0)
cv2.imshow('Contour', contour_image)
#cv2.imshow('Contour', img_copy)
cv2.imshow('Plot', plot)

cv2.waitKey(0)
##opening followed by closing after binarization!!!!!!!!
cv2.destroyAllWindows()
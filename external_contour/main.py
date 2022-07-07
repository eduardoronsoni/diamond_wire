import numpy as np
import cv2
import matplotlib.pyplot as plt
from itertools import chain
from collections import Counter


def rescale(img, pct):
    """
    Rescale the image
    pct - percentage of the new image size (both in height and width)
    when compared to the original size
    img - image you want to change the size

    """

    scale_pct = pct
    w = int(img.shape[1] * scale_pct / 100)  # width
    h = int(img.shape[0] * scale_pct / 100)  # height
    dim = (w, h)  # new image dimension

    imgResized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    return imgResized


def crop(img, x, y):
    """
    Crop the image
    x - maximum x coordinate of pixels (width)
    y - maximum height you want
    img - image you want to change the size

    """

    w = int(img.shape[1])  # width
    h = int(img.shape[0])  # heigth

    img = img[0:y, 0:x]

    return img


path = '../images/fio_2.1.tif'  # path of images directory

img = cv2.imread(path, 0)  # get grayscale image

img = rescale(img, 50)

# Copying the images for drawing purposes
img_copy = img.copy()
img_draw = img.copy()
img_point = img.copy()

# img = crop(img,50,100)

print('Shape of image after rescaling and cropping: ', img.shape)

# Binarization
_, binary = cv2.threshold(img, 112, 255, cv2.THRESH_BINARY)

# Bilateral Blur
bilateral = cv2.bilateralFilter(binary, 5, 75, 75)

# Finding Contour
contours, hierarchy = cv2.findContours(
    bilateral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
largest_contours = sorted(contours, key=cv2.contourArea)[-1:]
cv2.drawContours(img_copy, largest_contours, -1, (0, 255, 0), 2)

# type of largest contours
# python list with all the contours in the image. Each individual contour is a numpy array of (x,y) coordinates of boundary points

print(len(largest_contours))

# looping through list(only 1 array on the list)
for contour in largest_contours:

    print('shape :', contour.shape)
    print('dimension: ', contour.ndim)
    max = 0
    upper_min = 0  # local minimum of the "lower" edge for nominal diameter
    min = contour.max()
    lower_min = contour.max()  # local minimum of the "upper" edge for nominal diameter


# looping through every pixel of the contour
    for i in np.ndindex(contour.shape[:2]):

        # print('i: ', i[0])  # [0])
        # print('contour i: ', contour[i])  # [1])
        # print('np index: ', np.ndindex(contour.shape[:2]).max())

        if contour[i][1] > max:
            max = contour[i][1]
            x_max = contour[i][0]

        if contour[i][1] < min:
            min = contour[i][1]
            x_min = contour[i][0]

    max_diam = max - min


for i in np.ndindex(contour.shape[:2]):
    # delimitating a workspace
    if ((contour[i][1] >= min) & (contour[i][1] <= (min + abs(max_diam - max)/2)) & (contour[i][0] >= x_max)):
        if contour[i][1] >= upper_min:
            upper_min = contour[i][1]
            x_upper = contour[i][0]

    if ((contour[i][1] <= max) & (contour[i][1] >= (max - abs(max_diam - max)/2)) & (contour[i][0] >= x_min)):
        if contour[i][1] <= lower_min:
            lower_min = contour[i][1]
            x_lower = contour[i][0]

    nominal_diam = abs(lower_min - upper_min)

edges = np.array([[[x_max, max], [x_min, min]]])
cv2.drawContours(img_draw, edges, -1, (0, 0, 255), 2)
max_point = cv2.circle(img_point, (x_max, max), radius=5,
                       color=(255, 0, 0), thickness=-1)
min_point = cv2.circle(img_point, (x_min, min), radius=5,
                       color=(255, 0, 0), thickness=-1)

upper_diam = cv2.circle(img_point, (x_upper, upper_min), radius=5,
                        color=(0, 255, 0), thickness=-1)
lower_diam = cv2.circle(img_point, (x_lower, lower_min), radius=5,
                        color=(0, 255, 0), thickness=-1)

print('upper diam: ', upper_min)
print('lower diam: ', lower_min)
print('max y: ', max)
print('min y: ', min)

# Showing Images
cv2.imshow('Contours Image', img_copy)
cv2.imshow('Test Image', img_draw)
cv2.imshow('Max Point', img_point)
cv2.waitKey(0)

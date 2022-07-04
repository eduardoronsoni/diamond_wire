import numpy as np
import cv2
import matplotlib.pyplot as plt
from itertools import chain


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
    min = contour.max()

    for i in np.ndindex(contour.shape[:2]):

        #print('i: ', i[0])
        print('contour i: ', contour[i])  # [1])

        if contour[i][1] > max:
            max = contour[i][1]
            x_max = contour[i][0]

        if contour[i][1] < min:
            min = contour[i][1]
            x_min = contour[i][0]

    diam = max - min
    edges = np.array([[[x_max, max], [x_min, min]]])
    cv2.drawContours(img_draw, edges, -1, (0, 0, 255), 2)

    print('max y: ', max)
    print('min y: ', min)

# Showing Images
cv2.imshow('Contours Image', img_copy)
cv2.imshow('Test Image', img_draw)
cv2.waitKey(0)

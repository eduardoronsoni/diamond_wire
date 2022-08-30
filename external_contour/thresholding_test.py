import numpy as np
import cv2
import matplotlib.pyplot as plt
from itertools import chain
from collections import Counter
import sys


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


def amplification(n):
    """
    Function to transform value between units of measurement 
    number of pixels ------>  µm
    x pixels = y µm
    """
    factor = 0

    if n == 50:
        # factor*pixel = µm ----------> factor = µm/pixel
        factor = (2.63)

    if n == 250:
        factor = (0.5128)

    return factor


# -----------------------------------------INICIALIZING IMAGE----------------------------------------------------------------------------------

path = "D:\diamond_wire\images\Fio_2.1.tif"  # path of images directory

img = cv2.imread(path, 0)  # get grayscale image

pct = 50  # size percentage of the original image
img = rescale(img, pct)

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


cv2.imshow('Contours Image', img_copy)
cv2.imshow('Test Image', img_draw)
cv2.imshow('Max Point', img_point)
cv2.waitKey(0)

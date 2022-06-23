import numpy as np
import cv2
import matplotlib.pyplot as plt


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

    img = img[(0:y), (0:x)]

    return img


path = '../images/fio_2.1.tif'  # path of images directory

img = cv2.imread(path, 0)  # get grayscale image

img = rescale(img, 50)


print(img.shape[0])

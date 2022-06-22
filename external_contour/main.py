import numpy as np
import cv2
import matplotlib.pyplot as plt
import os


def rescale(img, pct):
    """ 
    Rescale the image
    pct - percentage of the new image size (both in height and width) 
    when compared to the original size
    img - image you want to change the size

    """

    scale_pct = pct
    w = int(img.shape[1] * scale_pct / 100)
    h = int(img.shape[0] * scale_pct / 100)
    dim = (w, h)

    imgResized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    return imgResized


path = '../images/fio_2.1.tif'  # path of images directory

img = cv2.imread(path, 0)  # get grayscale image


print(img.shape)

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

path = "D:\diamond_wire\images\Fio_10.tif"  # path of images directory

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


edges = cv2.Canny(bilateral,50,150,apertureSize=3)

# type of largest contours
# python list with all the contours in the image. Each individual contour is a numpy array of (x,y) coordinates of boundary points

lines_list =[]
lines = cv2.HoughLinesP(
            edges, # Input edge image
            1, # Distance resolution in pixels
            np.pi/180, # Angle resolution in radians
            threshold=100, # Min number of votes for valid line
            minLineLength=5, # Min allowed length of line
            maxLineGap=10 # Max allowed gap between line for joining them
            )

# Iterate over points
for points in lines:
      # Extracted points nested in the list
    x1,y1,x2,y2=points[0]
    # Draw the lines joing the points
    # On the original image
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
    # Maintain a simples lookup list for points
    lines_list.append([(x1,y1),(x2,y2)])

# print(lines_list)
# #print(len(largest_contours))

# print(len(lines_list))

# for item in lines_list:
#     for a in item:
#         print(a[1])##getting all y in list of lines from hough transform

# ----------------------------------------USER MICROSCOPE ZOOM IMPUT------------------------------------------------------------
values_list = [50, 250]
print(type(values_list))
value = input(
    f'Insira o valor da escala do microscópio de acordo com a lista a seguir: {values_list} \n ')
print(f'Você inseriu o valor {value} ')
value = int(value)

if value in values_list:
    print(f'Valor válido ...')
else:
    print(
        f'ERRO: Valor inserido não disponível na lista de valores, código será encerrado')
    sys.exit()

fct = (amplification(value))/(pct/100)
# ------------------------------------------------LOOPING THROUGH LIST (ONLY 1 ARRAY ON THE LIST)-------------------------------------
for contour in largest_contours:

    print('shape :', contour.shape)
    print('dimension: ', contour.ndim)
    max = 0

    min = contour.max()

    list_contours = []

# -------------------------------------------------LOOPING THROUGH EVERY ITEM OF  THE CONTOUR-----------------------------------------
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

        list_contours.append((contour[i][0], contour[i][1]))

    max_diam = abs(max - min)
    max_radius = abs(max - min)/2

    upper_min = min  # local minimum of the "lower" edge for nominal diameter
    lower_min = contour.max()  # local minimum of the "upper" edge for nominal diameter

    for item in lines_list:##getting all y in list of lines from hough transform
        for a in item:
            if ((a[1] >= min) & (a[1] <= (min + max_radius)) & (a[0] >=10) & (a[0] <= (img.shape[1] - 10))):
                if a[1] >= upper_min: 
                    print('veio no primeiro loop')
                    upper_min = a[1]
                    x_upper = a[0]


            if ((a[1] <= max) & (a[1] >= (max - max_radius)) & (a[0] >= 10) & (a[0] <= (img.shape[1] - 10))):
                if a[1] <= lower_min:
                    print('Veio no segundo loop')
                    lower_min = a[1]
                    x_lower = a[0]
    
    nominal_diam = abs(lower_min - upper_min)


#     for i in np.ndindex(contour.shape[:2]):
#         # delimitating a workspace
#         if ((contour[i][1] >= min) & (contour[i][1] <= (min + max_radius)) & (contour[i][0] >= 10) & (contour[i][0] <= (img.shape[1] - 10))):
#             if contour[i][1] > upper_min:
#                 upper_min = contour[i][1]
#                 x_upper = contour[i][0]

#         if ((contour[i][1] <= max) & (contour[i][1] >= (max - max_radius)) & (contour[i][0] >= 10) & (contour[i][0] <= (img.shape[1] - 10))):
#             if contour[i][1] <= lower_min:
#                 lower_min = contour[i][1]
#                 x_lower = contour[i][0]

# nominal_diam = abs(lower_min - upper_min)


# ---------------------------------------LOOPING THROUGH EVERY PIXEL-------------------------------------------------------
# list_upper = []
# list_lower = []

# # i = 0
# # j = 0
# for x in range(img.shape[1]):  # width
#     for y in range(img.shape[0]):  # height

#         if y <= upper_min:
#             if (x, y) in (list_contours):
#                 # i += 1
#                 list_upper.append(y)

#         if y >= lower_min:
#             if (x, y) in (list_contours):
#                 # j += 1
#                 list_lower.append(y)


# def Average(lst):
#     return sum(lst) / len(lst)


# average_upper = Average(list_upper)
# average_lower = Average(list_lower)

# ---------------------------------------PRINTING RESULTS----------------------------------------------------------------------
# print('List of Contours: ', list_contours)
# print('(All the measures showed below are in number of pixels)')
# print('upper nominal: ', upper_min)
# print('lower nominal: ', lower_min)
print(f'minimum diameter:{fct*nominal_diam} µm')
# print(f'mean diameter: {fct*(round(abs(average_lower - average_upper)))} µm')
print(f'maximum diameter:{fct*max_diam} µm')
# print('max y: ', max)
# print('min y: ', min)
# print('mean upper :', round(average_upper))
# print('mean lower :', round(average_lower))


edges = np.array([[[x_max, max], [x_min, min]]])
nominal = np.array([[[x_upper, upper_min], [x_lower, lower_min]]])
# mean = np.array([[[round((img.shape[1])/2), int(average_upper)],
#                 [round((img.shape[1])/2), int(average_lower)]]])

cv2.drawContours(img_draw, edges, -1, (0, 0, 255), 2)
cv2.drawContours(img_draw, nominal, -1, (255, 0, 0), 2)
# cv2.drawContours(img_draw, mean, -1, (0, 255, 0), 2)

max_point = cv2.circle(img_point, (x_max, max), radius=5,
                       color=(255, 0, 0), thickness=-1)
min_point = cv2.circle(img_point, (x_min, min), radius=5,
                       color=(255, 0, 0), thickness=-1)
upper_diam = cv2.circle(img_point, (x_upper, upper_min), radius=5,
                        color=(0, 255, 0), thickness=-1)
lower_diam = cv2.circle(img_point, (x_lower, lower_min), radius=5,
                        color=(0, 255, 0), thickness=-1)
# upper_mean_diam = cv2.circle(img_point, (240, int(round(average_upper))), radius=5,
#                             color=(0, 0, 255), thickness=-1)
# lower_mean_diam = cv2.circle(img_point, (240, int(round(average_lower))), radius=5,
#                             color=(0, 0, 255), thickness=-1)

# ---------------------------------------PLOTTING IMAGES---------------------------------------------------------------------
cv2.imshow('Contours Image', img_copy)
cv2.imshow('Test Image', img_draw)
cv2.imshow('Max Point', img_point)
cv2.imshow('detectedLines.png',img)
cv2.waitKey(0)

cv2.waitKey(0)

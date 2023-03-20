import cv2
import numpy as np
import matplotlib.pyplot as plt


path = "D:\diamond_wire\images\Fio_2.1.tif"
masking_path = "D:\diamond_wire\images\mask_2.1.tif"

imgBig = cv2.imread(path)
assert imgBig is not None, "file could not be read, check with os.path.exists()"


scale_percent = 50  # percent of original size
w = int(imgBig.shape[1] * scale_percent / 100)
h = int(imgBig.shape[0] * scale_percent / 100)
dim = (w, h)

# resize image
imgResized = cv2.resize(imgBig, dim, interpolation=cv2.INTER_AREA)
print('Tamanho Img Resized', imgResized.shape)

#changing resized image to grayscale to make it work - same number of channels as the mask image
gray = cv2.cvtColor(imgResized, cv2.COLOR_BGR2GRAY)


mask = cv2.imread(masking_path, cv2.IMREAD_GRAYSCALE)

print('Grayscale Image Shape',gray.shape)
print('Mask Shape', mask.shape)

#masking operation
img = cv2.bitwise_and(gray, mask)

#Appling CLAHE - Adaptive Histogram Equalization for enhancing contrast in the image
clahe= cv2.createCLAHE(clipLimit = 4.0, tileGridSize=(8,8))
cl_img = clahe.apply(img)

#Applying Filter to Denoise the CLAHE image - Despeckle - https://stackoverflow.com/questions/5680429/how-to-implement-despeckle-in-opencv
blur = cv2.bilateralFilter(cl_img,9,75,75)

#Canny Edge - Trying to get edges of the grains
canny = cv2.Canny(blur, 100, 200)#the standard is 100,200

#showing results
cv2.imshow('Masked', img)
cv2.imshow('CLAHE Img',cl_img)
cv2.imshow('After Blurring - Gaussian Filter', blur)
cv2.imshow('Canny Edes Image', canny)
cv2.waitKey(0)
cv2.destroyAllWindows()
import cv2
import numpy as np


path = "D:\diamond_wire\images\Fio_2.1.tif"
masking_path = "D:\diamond_wire\images\mask_2.1.tif"

imgBig = cv2.imread(path)


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

print('Tamanho Imagem',gray.shape)
print('Tamanho mascara', mask.shape)

img = cv2.bitwise_and(gray, mask)


cv2.imshow('Masked', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
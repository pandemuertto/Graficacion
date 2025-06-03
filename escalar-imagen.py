# Este código carga una imagen en escala de grises y muestra dos formas distintas de escalarla (reducir su tamaño). 
# Primero, intenta escalarla manualmente duplicando las coordenadas de píxeles, y luego utiliza 
# la función cv.resize() de OpenCV para reducir su tamaño a la mitad. 
# Al final, se muestran tanto la imagen original como la imagen escalada

import cv2 as cv
import numpy as np

#traslada una imagen
img = cv.imread('senku.jpg', 0)
x , y = img.shape
scale_x, scale_y = 2, 2
scaled_img = np.zeros((int (x * scale_y), int(y * scale_x)), np.uint8)
for i in range(x):
    for j in range(y):
        scaled_img[i*2, j*2] = img[i, j]

# Definir el factor de escala
scale_x, scale_y = 0.5, 0.5

# Aplicar el escalado usando cv.resize()
scaled_img = cv.resize(img, None, fx=scale_x, fy=scale_y)
    
cv.imshow('Imagen original', img)
cv.imshow('Imagen escalada (modo raw)', scaled_img)

cv.waitKey(0)
cv.destroyAllWindows
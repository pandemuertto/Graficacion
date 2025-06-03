# Este código utiliza OpenCV para cargar una imagen en color y mostrarla en diferentes formatos: 
# escala de grises, modelo de color HSV, y una reconversión de escala de grises nuevamente a formato BGR. 
# Esto permite comparar cómo se representa una imagen en distintos espacios de color y cómo se comportan 
# las conversiones entre ellos.

import numpy as np
import cv2 as cv

img = cv.imread('senku.jpg', 1)  # Imagen en color BGR

# Verifica si la imagen se cargó correctamente
if img is None:
    print("No se pudo cargar la imagen.")
    exit()

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # Convierte a escala de grises
img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)    # Convierte a HSV
img_bgr_from_gray = cv.cvtColor(img_gray, cv.COLOR_GRAY2BGR)  # Reconversión válida a BGR

# Mostrar imágenes con nombres diferentes
cv.imshow('Original', img)
cv.imshow('Gris', img_gray)
cv.imshow('HSV', img_hsv)
cv.imshow('Gris a BGR', img_bgr_from_gray)

cv.waitKey(0)
cv.destroyAllWindows()

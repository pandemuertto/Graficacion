import numpy as np   # Importa la librería NumPy, útil para trabajar con arreglos y operaciones numéricas.
import cv2 as cv     # Importa la librería OpenCV, que se utiliza para procesamiento de imágenes.

img = cv.imread('bts.jfif', 1)  # Carga la imagen '1.png' en color (1 para color, 0 para escala de grises).

img2=cv.cvtColor(img, cv.COLOR_BGR2GRAY) # Convierte la imagen a escala de grises.
img2=cv.cvtColor(img, cv.COLOR_RGB2GRAY) # Convierte la imagen a color.    

img3=cv.cvtColor(img, cv.COLOR_GRAY2BGR555) # Convierte la imagen a RGB.
img3=cv.cvtColor(img3, cv.COLOR_BGR5552GRAY) # Convierte la imagen a BGR

img4=cv.cvtColor(img, cv.COLOR_BGR2HSV) # Convierte la imagen a HSV.
# Muestra la imagen en una ventana con el título 'img'. 
cv.imshow('img', img)
cv.imshow('img', img2)
cv.imshow('img', img3)
cv.imshow('img', img4)

# Espera a que el usuario presione cualquier tecla para continuar.
cv.waitKey()

# Cierra todas las ventanas creadas por OpenCV.
cv.destroyAllWindows()
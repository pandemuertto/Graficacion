# Archivo: convulusion.py

```python
# Este programa en Python utiliza OpenCV y NumPy para realizar dos operaciones 
# clave de procesamiento de imágenes:
# Escalado manual de una imagen en escala de grises, duplicando su tamaño al copiar cada píxel a una 
# nueva ubicación más grande sin interpolación.
# Aplicación de una convolución manual con un filtro de promedio 3x3, que suaviza la imagen escalada 
# al calcular el valor de cada píxel como el promedio de sus vecinos.

import numpy as np
import cv2 as cv

# Cargar imagen en escala de grises
img = cv.imread('senku.jpg', 0)
x, y = img.shape

# Escalado de la imagen (duplicando el tamaño)
scale_x, scale_y = 2, 2
scale_img = np.zeros((x * scale_x, y * scale_y), dtype=np.uint8)

for i in range(x):
    for j in range(y):
        scale_img[i * scale_x, j * scale_y] = img[i, j]

# Definir el kernel de promedio 3x3
kernel = np.ones((3, 3), dtype=np.float32) / 9

# Crear la imagen resultante
conv_img = np.zeros_like(scale_img)

# Aplicar convolución manualmente
for i in range(1, scale_img.shape[0] - 1):
    for j in range(1, scale_img.shape[1] - 1):
        suma = 0
        for ki in range(-1, 2):  # Rango -1 a 1 para centrar el kernel
            for kj in range(-1, 2):
                suma += scale_img[i + ki, j + kj] * kernel[ki + 1, kj + 1]
        conv_img[i, j] = np.clip(suma, 0, 255)  # Asegurar valores válidos de pixel

# Mostrar imágenes
cv.imshow('Imagen Original', img)
cv.imshow('Imagen Escalada', scale_img)
cv.imshow('Imagen Convolucionada', conv_img)

cv.waitKey(0)
cv.destroyAllWindows()


```
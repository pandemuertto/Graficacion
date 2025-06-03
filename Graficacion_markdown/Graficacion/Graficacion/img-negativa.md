# Archivo: img-negativa.py

```python
# El código realiza el procesamiento básico de una imagen utilizando OpenCV. 
# Primero, carga una imagen en color desde el archivo 'senku.jpg', luego la convierte a escala de grises. 
# A continuación, aplica un efecto de negativo fotográfico, invirtiendo los valores de brillo de cada píxel. 
# Finalmente, muestra tanto la imagen original como la transformada en dos ventanas separadas.

import cv2 as cv
import numpy

img=cv.imread('senku.jpg',1)
img2=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
print(img2.shape[:2])
x ,y=img2.shape[:2]
for i in range(x):
    for j in range(y):
        img2[i,j]=255-img2[i,j]

cv.imshow('img',img)
cv.imshow('img2',img2)
# Espera a que el usuario presione cualquier tecla para continuar.
cv.waitKey()

# Cierra todas las ventanas creadas por OpenCV.
cv.destroyAllWindows()

```
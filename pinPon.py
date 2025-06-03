# Este programa utiliza OpenCV y NumPy para animar una pelotita verde que se mueve diagonalmente en una ventana y rebota. 
# La animación se logra dibujando y actualizando cuadros (frames) en un bucle, generando así el efecto de movimiento

import cv2 as cv
import numpy as np


for i in range(480):
    img = np.ones((500, 500, 3), dtype=np.uint8) * 255
    cv.circle(img, (0+i, 0+i), 20, (0, 234, 21), -1)
    cv.imshow('imag', img)
    cv.waitKey(10)   

for i in range(480):
    img = np.ones((500, 500, 3), dtype=np.uint8) * 255
    cv.circle(img, (480-i, 480-i), 20, (0, 234, 21), -1)
    cv.imshow('imag', img)
    cv.waitKey(10)
    
cv.waitKey(0)
cv.destroyAllWindows
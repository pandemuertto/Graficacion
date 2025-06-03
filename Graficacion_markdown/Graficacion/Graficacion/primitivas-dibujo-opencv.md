# Archivo: primitivas-dibujo-opencv.py

```python
# Este programa utiliza OpenCV para dibujar un mike wazowski con formas básicas (círculos, triángulos y líneas) 
# sobre un lienzo blanco. Las partes como la cabeza, ojos, brazos, piernas y orejas se representan mediante coordenadas precisas. 
# La figura se muestra en una ventana gráfica.

import cv2 as cv
import numpy as np

img = np.ones((500, 500, 3), dtype=np.uint8) * 255

# for i in range(400):
#     img = np.ones((500, 500, 3), dtype=np.uint8) * 255
#     cv.circle(img, (0+i, 0+i), 20, (0, 234, 21), -1)
#     cv.imshow('imag', img)
#     cv.waitKey(40)
    
cv.circle(img, (250, 250), 100, (0, 255, 0), -1) #circulo grande verde
cv.circle(img, (250, 250), 50, (0, 0, 0), -1) #circulo negro
cv.circle(img, (250, 250), 40, (255,255,255), -1) #circulo blanco chiquito
cv.circle(img, (250, 250), 20, (10,150,50), -1) #circulo verde chiquito
# cv.circle(img, (250,250), 100, (0,0,0), 3)

#triangulito izquierdo
pts = np.array([[170, 200], [200, 200], [180, 150]], np.int32) #[esquina inferior izquierda],[esqui infer derecha], [punta del triangulo] # Triángulo centrado
pts = pts.reshape((-1, 1, 2))
cv.polylines(img, [pts], True, (230, 240, 230), 3)  # Borde negro
cv.fillPoly(img, [pts], (240, 250, 240))

#tringulito derecho
pts1 = np.array([[330, 200], [300, 200], [320, 150]], np.int32) #[esquina inferior izquierda],[esqui infer derecha], [punta del triangulo] # Triángulo centrado
pts1 = pts1.reshape((-1, 1, 2))
cv.polylines(img, [pts1], True, (230, 240, 230), 3)  # Borde
cv.fillPoly(img, [pts1], (240, 250, 240))

# patita izquierda
cv.line(img, (200, 300), (200, 400), (0, 255, 0), 20)
cv.line(img, (200, 400), (170, 420), (0, 255, 0), 20)

# patita derecha
cv.line(img, (300, 300), (300, 400), (0, 255, 0), 20)
cv.line(img, (300, 400), (330, 420), (0, 255, 0), 20)

#manita izquierda
cv.line(img, (170, 250), (120, 300), (0, 255, 0), 20)

#manita derecha
cv.line(img, (330, 250), (370, 300), (0, 255, 0), 20)

cv.imshow('imag', img)

cv.waitKey(0)
cv.destroyAllWindows()
```
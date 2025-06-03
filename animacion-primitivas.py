# Este programa utiliza OpenCV para crear una animación básica de mike wazowski, simulando el abrir y cerrar de su ojo de forma repetitiva. 
# La figura se construye con formas geométricas simples (círculos, triángulos y líneas), y se alternan dos estados 
# visuales para generar el efecto animado: ojo abierto y ojo cerrado. 
# La animación se muestra en un bucle continuo hasta que se interrumpe manualmente.

import cv2 as cv
import numpy as np

# img = np.ones((500, 500, 3), dtype=np.uint8) * 255

# # for i in range(400):
# #     img = np.ones((500, 500, 3), dtype=np.uint8) * 255
# #     cv.circle(img, (0+i, 0+i), 20, (0, 234, 21), -1)
# #     cv.imshow('imag', img)
# #     cv.waitKey(40)
    
# cv.circle(img, (250, 250), 100, (0, 255, 0), -1) #circulo grande verde
# cv.circle(img, (250, 250), 50, (0, 0, 0), -1) #circulo negro
# cv.circle(img, (250, 250), 40, (255,255,255), -1) #circulo blanco chiquito
# cv.circle(img, (250, 250), 20, (10,150,50), -1) #circulo verde chiquito
# # cv.circle(img, (250,250), 100, (0,0,0), 3)

x = 0
y = 1
#abrir y cerrar ojo
while True:
    img = np.ones((500, 500, 3), dtype=np.uint8) * 255
    
    if x == 0:
        cv.waitKey(120)
        x = 1
        cv.circle(img, (250, 250), 100, (0, 255, 0), -1) #circulo grande verde
        cv.circle(img, (250, 250), 50, (0, 0, 0), -1) #circulo negro
        cv.circle(img, (250, 250), 40, (255,255,255), -1) #circulo blanco chiquito
        cv.circle(img, (250, 250), 20, (10,150,50), -1) #circulo verde chiquito
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
        cv.waitKey(120)
    if x == 1:
        cv.waitKey(120)
        x = 0
        cv.circle(img, (250, 250), 100, (0, 255, 0), -1) #circulo grande verde
        cv.line(img, (200, 250), (300, 250), (0, 0, 0), 10)
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
        cv.waitKey(120)


# #triangulito izquierdo
# pts = np.array([[170, 200], [200, 200], [180, 150]], np.int32) #[esquina inferior izquierda],[esqui infer derecha], [punta del triangulo] # Triángulo centrado
# pts = pts.reshape((-1, 1, 2))
# cv.polylines(img, [pts], True, (230, 240, 230), 3)  # Borde negro
# cv.fillPoly(img, [pts], (240, 250, 240))

# #tringulito derecho
# pts1 = np.array([[330, 200], [300, 200], [320, 150]], np.int32) #[esquina inferior izquierda],[esqui infer derecha], [punta del triangulo] # Triángulo centrado
# pts1 = pts1.reshape((-1, 1, 2))
# cv.polylines(img, [pts1], True, (230, 240, 230), 3)  # Borde
# cv.fillPoly(img, [pts1], (240, 250, 240))

# # patita izquierda
# cv.line(img, (200, 300), (200, 400), (0, 255, 0), 20)
# cv.line(img, (200, 400), (170, 420), (0, 255, 0), 20)

# # patita derecha
# cv.line(img, (300, 300), (300, 400), (0, 255, 0), 20)
# cv.line(img, (300, 400), (330, 420), (0, 255, 0), 20)

# #manita izquierda
# cv.line(img, (170, 250), (120, 300), (0, 255, 0), 20)

# #manita derecha
# cv.line(img, (330, 250), (370, 300), (0, 255, 0), 20)

cv.imshow('imag', img)

cv.waitKey(60)
cv.destroyAllWindows()
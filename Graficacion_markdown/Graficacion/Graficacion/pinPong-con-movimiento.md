# Archivo: pinPong-con-movimiento.py

```python
# Este programa en Python simula una pelotita de pin pong que rebota dentro de un recuadro, 
# utilizando OpenCV para capturar video en tiempo real desde la cámara. 
# La pelotita se mueve automáticamente, pero cada vez que se detecta movimiento significativo 
# frente a la cámara (por ejemplo, una mano agitándose), la dirección del rebote cambia aleatoriamente. 
# Esto se logra comparando los cuadros consecutivos del video y detectando diferencias que indiquen movimiento.


import numpy as np
import cv2 as cv

# Captura de video
cap = cv.VideoCapture(0)

# Tamaño del frame
ret, frame = cap.read()
height, width = frame.shape[:2]

# Posición y velocidad inicial de la pelotita
ball_pos = np.array([100, 150], dtype=np.int32)
ball_radius = 20
vx, vy = 5, 5  # velocidad inicial

# Cuadro de rebote
box_margin = 20
box_top_left = (box_margin, box_margin)
box_bottom_right = (width - box_margin, height - box_margin)

# Primer frame en escala de grises
prev_gray = cv.cvtColor(cv.flip(frame, 1), cv.COLOR_BGR2GRAY)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv.flip(frame, 1)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Dibujar el cuadrado azul
    cv.rectangle(frame, box_top_left, box_bottom_right, (255, 0, 0), 5)

    # Detectar movimiento por diferencia de frames
    diff = cv.absdiff(prev_gray, gray)
    _, thresh = cv.threshold(diff, 25, 255, cv.THRESH_BINARY)
    motion_detected = np.sum(thresh) > 500000  # umbral para saber si hubo "movimiento fuerte"

    if motion_detected:
        vx, vy = np.random.choice([-5, 5]), np.random.choice([-5, 5])

    # Actualizar posición
    ball_pos[0] += vx
    ball_pos[1] += vy

    # Rebotar en los bordes del cuadro
    if ball_pos[0] - ball_radius <= box_margin or ball_pos[0] + ball_radius >= width - box_margin:
        vx *= -1
    if ball_pos[1] - ball_radius <= box_margin or ball_pos[1] + ball_radius >= height - box_margin:
        vy *= -1

    # Dibujar la pelotita
    cv.circle(frame, tuple(ball_pos), ball_radius, (0, 255, 0), -1)

    # Mostrar el frame
    cv.imshow("Pelotita rebotando", frame)

    # Actualizar el frame anterior
    prev_gray = gray.copy()

    if cv.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv.destroyAllWindows()

```
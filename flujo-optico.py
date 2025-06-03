# Este programa utiliza OpenCV para realizar seguimiento de movimiento en video en tiempo real, 
# empleando el algoritmo de flujo óptico de Lucas-Kanade. 
# Se simula una pelotita que se mueve por la pantalla y cambia de posición según el movimiento detectado 
# entre cuadros consecutivos. Además, se establece una red de puntos que también se rastrean para visualizar 
# el flujo del entorno. La posición de la pelotita y de cada punto se actualiza constantemente, 
# y se muestran visualmente sus desplazamientos en pantalla

import numpy as np
import cv2 as cv

# Iniciar la captura de video desde la cámara
cap = cv.VideoCapture(0)

# Parámetros para el flujo óptico Lucas-Kanade
lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

# Leer primer frame para iniciar variables
_, vframe = cap.read()
vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)

# Red de puntos
p0 = np.array([(100,100), (200,100), (300,100), (400,100), (500,100),
               (100,200), (200,200), (300,200), (400,200), (500,200),
               (100,300), (200,300), (300,300), (400,300), (500,300),
               (100,400), (200,400), (300,400), (400,400), (500,400)], dtype=np.float32)
p0 = p0[:, np.newaxis, :]

mask = np.zeros_like(vframe)

# Leer otro frame para pelotita
ret, first_frame = cap.read()
prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)

# Pelotita
h, w = first_frame.shape[:2]
ball_pos = np.array([[w//2, h//2]], dtype=np.float32)
ball_pos = ball_pos[:, np.newaxis, :]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    frame = cv.flip(frame, 1)
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Calcular flujo óptico para pelotita
    new_ball_pos, st_ball, err_ball = cv.calcOpticalFlowPyrLK(prev_gray, gray_frame, ball_pos, None, **lk_params)

    p1, st, err = cv.calcOpticalFlowPyrLK(vgris, gray_frame, p0, None, **lk_params)

    if new_ball_pos is not None:
        a, b = new_ball_pos.ravel()
        a = max(20, min(a, w - 20))
        b = max(20, min(b, h - 20))
        ball_pos = np.array([[a, b]], dtype=np.float32)[np.newaxis, :]

    a, b = ball_pos.ravel()
    cv.putText(frame, f'({int(a)}, {int(b)})', (int(a - 30), int(b - 30)), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    frame = cv.circle(frame, (int(a), int(b)), 20, (0, 255, 0), -1)
    cv.rectangle(frame, (20, 20), (w - 20, h - 20), (234, 43, 34), 5)

    # Mostrar ventana principal
    cv.imshow('Pelota en movimiento', frame)

    prev_gray = gray_frame.copy()

    if p1 is None:
        vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)
        p0 = np.array([(100,100), (200,100), (300,100), (400,100)], dtype=np.float32)
        p0 = p0[:, np.newaxis, :]
        mask = np.zeros_like(vframe)
        cv.imshow('ventana', frame)
    else:
        bp1 = p1[st == 1]
        bp0 = p0[st == 1]

        for i, (nv, vj) in enumerate(zip(bp1, bp0)):
            a1, b1 = (int(x) for x in nv.ravel())
            c1, d1 = (int(x) for x in vj.ravel())
            dist = np.linalg.norm(nv.ravel() - vj.ravel())

            print(i, dist)

            frame = cv.line(frame, (c1, d1), (a1, b1), (0, 0, 255), 2)
            frame = cv.circle(frame, (c1, d1), 2, (255, 0, 0), -1)
            frame = cv.circle(frame, (a1, b1), 3, (0, 255, 0), -1)

        cv.imshow('vent', frame)

    if cv.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv.destroyAllWindows()

# Archivo: filtro.py

```python
# Este programa usa OpenCV para capturar video en tiempo real desde la cámara y aplicar detección de rostros usando 
# un modelo preentrenado de tipo Haar Cascade. Cuando detecta un rostro, dibuja un rectángulo verde alrededor de él y 
# añade círculos con colores y posiciones específicas sobre el rostro, como si fuera un filtro de instagram 
# La ventana muestra continuamente el video con estos efectos hasta que se presiona la tecla q.

import numpy as np
import cv2 as cv


rostro = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

cap = cv.VideoCapture(0)
x = y = w = h = 0
count = 0

while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in rostros:
        m = int(h / 2)
        frame = cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        frame = cv.circle(frame, (x + int(w / 2), y + int(h / 2)), int(h / 8), (0, 0, 255), -1)
        frame = cv.circle(frame, (x + int(w / 8), y + int(h / 8)), int(h / 4), (255, 255, 0), -1)
        frame = cv.circle(frame, (x + int(7 * w / 8), y + int(h / 8)), int(h / 4), (255, 255, 0), -1)

    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()


```
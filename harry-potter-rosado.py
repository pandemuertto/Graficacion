# Este programa utiliza la cámara web y la biblioteca OpenCV para crear el efecto de una "capa de invisibilidad". 
# Detecta zonas de color rosado en tiempo real, y en lugar de mostrarlas, las reemplaza con una imagen de fondo 
# previamente capturada. Esto crea la ilusión de que los objetos (o ropa) de color rosa desaparecen del video 
# en vivo.

import cv2 
import numpy as np

# Captura de video desde la cámara
cap = cv2.VideoCapture(0)

# Permitir que la cámara se estabilice
cv2.waitKey(2000)

# Capturar el fondo durante unos segundos
ret, background = cap.read()
if not ret:
    print("Error al capturar el fondo.")
    cap.release()
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir el cuadro a espacio de color HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definir el rango de color rosado en HSV
    lower_pink = np.array([140, 50, 50])
    upper_pink = np.array([170, 255, 255])

    # Crear una máscara para el rosa
    mask = cv2.inRange(hsv, lower_pink, upper_pink)

    # Invertir la máscara para obtener las áreas que no son rosadas
    mask_inv = cv2.bitwise_not(mask)

    # Aplicar la máscara al frame original
    res1 = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # Aplicar la máscara al fondo
    res2 = cv2.bitwise_and(background, background, mask=mask)

    # Combinar ambos resultados
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    # Mostrar resultados
    cv2.imshow("Capa de Invisibilidad (Rosa)", final_output)
    cv2.imshow('Máscara', mask)

    # Presionar 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos
cap.release()
cv2.destroyAllWindows()
  
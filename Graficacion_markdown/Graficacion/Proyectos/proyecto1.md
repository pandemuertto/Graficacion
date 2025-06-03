# Archivo: proyecto1.py

```python
import cv2
import mediapipe as mp
import numpy as np
import random as r
import time

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Variables para el reconocimiento de palabras
palabra_actual = ""
tiempo_ultima_letra = time.time()
TIEMPO_ESPERA = 2  # segundos para confirmar una letra

# Función para verificar si un dedo está extendido
def dedo_extendido(landmarks, tip_id, pip_id):
    return landmarks[tip_id].y < landmarks[pip_id].y

def pulgar_extendido(landmarks):
    # Comparación más estricta para el pulgar - debe estar muy separado
    distancia_pulgar = abs(landmarks[4].x - landmarks[3].x)
    return distancia_pulgar > 0.05  # Más estricto

def calcular_distancia(punto1, punto2):
    return np.sqrt((punto1[0] - punto2[0])**2 + (punto1[1] - punto2[1])**2)

def calcular_angulo(p1, p2, p3):
    """Calcula el ángulo entre tres puntos"""
    v1 = np.array([p1[0] - p2[0], p1[1] - p2[1]])
    v2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])
    
    cosine_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)

# Función mejorada para reconocer letras y números
def reconocer_signo(hand_landmarks, frame):
    h, w, _ = frame.shape
    # Obtener coordenadas de los puntos clave en píxeles
    dedos = [(int(hand_landmarks.landmark[i].x * w), int(hand_landmarks.landmark[i].y * h)) for i in range(21)]
    
    # Obtener posiciones clave
    pulgar = dedos[4]
    indice = dedos[8]
    medio = dedos[12]
    anular = dedos[16]
    meñique = dedos[20]
    base_medio = dedos[9]
    base_indice = dedos[5]
    base_anular = dedos[13]
    base_meñique = dedos[17]
    muñeca = dedos[0]
    
    # Verificar qué dedos están extendidos
    dedos_extendidos = []
    dedos_extendidos.append(pulgar_extendido(hand_landmarks.landmark))
    dedos_extendidos.append(dedo_extendido(hand_landmarks.landmark, 8, 6))  # Índice
    dedos_extendidos.append(dedo_extendido(hand_landmarks.landmark, 12, 10))  # Medio
    dedos_extendidos.append(dedo_extendido(hand_landmarks.landmark, 16, 14))  # Anular
    dedos_extendidos.append(dedo_extendido(hand_landmarks.landmark, 20, 18))  # Meñique
    
    # Calcular distancias importantes
    dist_pulgar_indice = calcular_distancia(pulgar, indice)
    dist_pulgar_medio = calcular_distancia(pulgar, medio)
    dist_indice_medio = calcular_distancia(indice, medio)
    
    # Mostrar información de depuración
    dedos_info = f"Dedos: P:{int(dedos_extendidos[0])} I:{int(dedos_extendidos[1])} M:{int(dedos_extendidos[2])} A:{int(dedos_extendidos[3])} Me:{int(dedos_extendidos[4])}"
    cv2.putText(frame, dedos_info, (10, h-50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    
    # Mostrar distancia índice-medio para depuración
    dist_info = f"Dist I-M: {int(dist_indice_medio)}"
    cv2.putText(frame, dist_info, (10, h-30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    
    # RECONOCIMIENTO DE LETRAS ORIGINALES
    if indice[1] < medio[1] and medio[1] < anular[1] and anular[1] < meñique[1]:
        return "A"
    
    # NUEVAS LETRAS Y NÚMEROS - ORDEN ESPECÍFICO IMPORTA
    
    # Número 48: Todos los dedos extendidos EXCEPTO el meñique
    if (dedos_extendidos[0] and dedos_extendidos[1] and dedos_extendidos[2] and 
        dedos_extendidos[3] and not dedos_extendidos[4]):
        return "48"
    
    # Número 29: Todos los 5 dedos extendidos y separados
    elif (all(dedos_extendidos) and dist_indice_medio > 30 and 
          calcular_distancia(medio, anular) > 25):
        return "29"
    
    # Letra K: Índice y medio extendidos en V, pulgar entre ellos (más específico)
    elif (dedos_extendidos[1] and dedos_extendidos[2] and not dedos_extendidos[3] and 
          not dedos_extendidos[4] and not dedos_extendidos[0]):
        angulo_dedos = calcular_angulo(indice, base_indice, medio)
        if angulo_dedos > 40:  # V más abierta para K
            return "K"
    
    # Letra U: Índice y medio extendidos y JUNTOS (permitir pulgar ligeramente extendido)
    elif (dedos_extendidos[1] and dedos_extendidos[2] and not dedos_extendidos[3] and 
          not dedos_extendidos[4]):  # Quitamos la restricción del pulgar
        if dist_indice_medio < 35:  # Un poco más permisivo
            return "U"
    
    # Número 2: Índice y medio extendidos en V (permitir pulgar ligeramente extendido)
    elif (dedos_extendidos[1] and dedos_extendidos[2] and not dedos_extendidos[3] and 
          not dedos_extendidos[4]):  # Quitamos la restricción del pulgar
        if dist_indice_medio > 35:  # Separados en V para el 2
            return "2"
    
    # Letra D: Solo índice extendido, otros dedos cerrados
    elif (dedos_extendidos[1] and not dedos_extendidos[2] and not dedos_extendidos[3] and 
          not dedos_extendidos[4] and not dedos_extendidos[0]):
        return "D"
    
    # Letra I: Solo meñique extendido, otros dedos cerrados
    elif (not dedos_extendidos[1] and not dedos_extendidos[2] and not dedos_extendidos[3] and 
          dedos_extendidos[4] and not dedos_extendidos[0]):
        return "I"
    
    # Detectar gesto ofensivo (del código original)
    elif medio[1] < indice[1] and medio[1] < anular[1] and medio[1] < meñique[1] and pulgar[1] < indice[1]:
        return "GESTO_INAPROPIADO"
    
    return "Desconocido"

def procesar_palabra(letra_detectada):
    """Procesa las letras para formar palabras"""
    global palabra_actual, tiempo_ultima_letra
    
    tiempo_actual = time.time()
    
    if letra_detectada in ["D", "I", "A"] and letra_detectada != "Desconocido":
        if tiempo_actual - tiempo_ultima_letra > TIEMPO_ESPERA:
            palabra_actual += letra_detectada
            tiempo_ultima_letra = tiempo_actual
            
            # Verificar si se formó la palabra "DIA"
            if palabra_actual == "DIA":
                return "¡PALABRA COMPLETA: DIA!"
            elif len(palabra_actual) > 3:
                palabra_actual = letra_detectada  # Reiniciar si es muy larga
    
    # Limpiar palabra si pasa mucho tiempo sin detectar letras válidas
    if tiempo_actual - tiempo_ultima_letra > TIEMPO_ESPERA * 2:
        palabra_actual = ""
    
    return f"Palabra en progreso: {palabra_actual}"

# Función removida - círculo colorido eliminado

# Captura de video
cap = cv2.VideoCapture(0)  # Cambiado a 0 (cámara principal)

print("Reconocedor de Lengua de Señas Iniciado")
print("Letras reconocidas: A, D, I, K, U")
print("Números reconocidos: 2, 29, 48")
print("Palabra especial: DIA")
print("Presiona 'q' para salir, 'r' para reiniciar palabra")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)  # Efecto espejo
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Procesar con MediaPipe
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Dibujar conexiones de la mano
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Reconocer signo
            signo_detectado = reconocer_signo(hand_landmarks, frame)
            
            # Procesar palabra
            estado_palabra = procesar_palabra(signo_detectado)
            
            # Mostrar información en pantalla
            cv2.putText(frame, f"Signo: {signo_detectado}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, estado_palabra, (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    
    # Mostrar instrucciones
    cv2.putText(frame, "Presiona 'q': salir, 'r': reiniciar palabra", (10, frame.shape[0] - 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    cv2.imshow("Reconocedor de Lengua de Señas", frame)
    
    # Control de teclado
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        palabra_actual = ""
        print("Palabra reiniciada")

# Limpiar recursos
cap.release()
cv2.destroyAllWindows()
```
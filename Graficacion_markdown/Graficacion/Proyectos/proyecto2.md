# Archivo: proyecto2.py

```python
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np
import cv2
import mediapipe as mp
import threading
import time

class HandGestureController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Variables para control de cámara
        self.hand_x = 0.5
        self.hand_y = 0.5
        self.hand_z = 0.5
        self.gesture_active = False
        self.camera_enabled = False
        
        # Suavizado
        self.smoothing_factor = 0.7
        self.prev_x = 0.5
        self.prev_y = 0.5
        
    def count_fingers(self, landmarks):
        """Cuenta cuántos dedos están levantados"""
        finger_tips = [4, 8, 12, 16, 20]
        finger_mcp = [3, 6, 10, 14, 18]
        
        fingers = []
        
        # Pulgar
        if landmarks[finger_tips[0]].x > landmarks[finger_tips[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)
            
        # Otros dedos
        for i in range(1, 5):
            if landmarks[finger_tips[i]].y < landmarks[finger_mcp[i]].y:
                fingers.append(1)
            else:
                fingers.append(0)
                
        return fingers
    
    def start_camera(self):
        """Inicia el hilo de la cámara"""
        self.camera_enabled = True
        camera_thread = threading.Thread(target=self.update_from_camera, daemon=True)
        camera_thread.start()
    
    def update_from_camera(self):
        """Procesa la cámara en un hilo separado"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: No se pudo abrir la cámara")
            return
            
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print("Control de gestos activado!")
        
        while self.camera_enabled:
            success, image = cap.read()
            if not success:
                continue
                
            image = cv2.flip(image, 1)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.hands.process(image_rgb)
            
            image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        image_bgr, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )
                    
                    # Obtener posición
                    center_landmark = hand_landmarks.landmark[9]
                    raw_x = center_landmark.x
                    raw_y = center_landmark.y
                    
                    # Suavizar
                    self.hand_x = self.smoothing_factor * self.prev_x + (1 - self.smoothing_factor) * raw_x
                    self.hand_y = self.smoothing_factor * self.prev_y + (1 - self.smoothing_factor) * raw_y
                    
                    self.prev_x = self.hand_x
                    self.prev_y = self.hand_y
                    
                    # Contar dedos
                    fingers_up = self.count_fingers(hand_landmarks.landmark)
                    fingers_count = sum(fingers_up)
                    
                    # Detectar gestos
                    if fingers_count == 0:
                        self.gesture_active = False
                        cv2.putText(image_bgr, "PAUSED", (10, 30), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    elif fingers_count >= 4:
                        self.gesture_active = True
                        cv2.putText(image_bgr, "CONTROLLING", (10, 30), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    elif fingers_count == 1 and fingers_up[0] == 1:
                        # Reset
                        self.hand_x = 0.5
                        self.hand_y = 0.5
                        cv2.putText(image_bgr, "RESET", (10, 30), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                    
                    cv2.putText(image_bgr, f"Fingers: {fingers_count}", (10, 70), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            else:
                cv2.putText(image_bgr, "NO HAND", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                self.gesture_active = False
            
            cv2.imshow('Hand Control', image_bgr)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()

class Camera:
    def __init__(self):
        self.distance = 8.0
        self.rotation_x = 20.0  # Ángulo inicial para ver mejor
        self.rotation_y = 0.0
        self.target_rotation_x = 20.0
        self.target_rotation_y = 0.0
        self.smoothing = 0.15
        
    def update_from_gesture(self, hand_controller):
        if hand_controller.gesture_active:
            # Convertir posición de mano a rotación
            self.target_rotation_y = (hand_controller.hand_x - 0.5) * 360
            self.target_rotation_x = 20 + (hand_controller.hand_y - 0.5) * 120
        
        # Suavizar
        self.rotation_x += (self.target_rotation_x - self.rotation_x) * self.smoothing
        self.rotation_y += (self.target_rotation_y - self.rotation_y) * self.smoothing
        
        # Limitar rotación
        if self.rotation_x > 80:
            self.rotation_x = 80
        if self.rotation_x < -80:
            self.rotation_x = -80
    
    def apply(self):
        glLoadIdentity()
        glTranslatef(0, 0, -self.distance)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

def draw_mike_wazowski():
    """Dibuja Mike Wazowski simplificado pero visible"""
    
    # Cuerpo principal (esfera verde)
    glColor3f(0.3, 0.9, 0.4)
    glPushMatrix()
    glScalef(1.0, 1.2, 1.0)
    draw_sphere(1.5, 16, 16)  # Menos subdivisiones para mejor rendimiento
    glPopMatrix()
    
    # Ojo grande (esfera blanca)
    glColor3f(0.95, 0.95, 0.95)
    glPushMatrix()
    glTranslatef(0, 0.3, 1.3)
    draw_sphere(0.8, 12, 12)
    glPopMatrix()
    
    # Pupila (esfera negra)
    glColor3f(0.1, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(0, 0.3, 2.0)
    draw_sphere(0.3, 8, 8)
    glPopMatrix()
    
    # Brillo en el ojo
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(0.15, 0.45, 2.2)
    draw_sphere(0.1, 6, 6)
    glPopMatrix()
    
    # Boca (esfera roja)
    glColor3f(0.9, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(0, -0.5, 1.2)
    glScalef(0.4, 0.2, 0.3)
    draw_sphere(0.6, 8, 8)
    glPopMatrix()
    
    # Cuernos
    glColor3f(0.2, 0.7, 0.3)
    # Izquierdo
    glPushMatrix()
    glTranslatef(-0.8, 1.8, 0)
    draw_cone(0.1, 0.4, 8)
    glPopMatrix()
    
    # Derecho
    glPushMatrix()
    glTranslatef(0.8, 1.8, 0)
    draw_cone(0.1, 0.4, 8)
    glPopMatrix()
    
    # Brazos
    glColor3f(0.3, 0.9, 0.4)
    # Izquierdo
    glPushMatrix()
    glTranslatef(-1.2, 0.2, 0)
    glRotatef(30, 0, 0, 1)
    draw_cylinder(0.2, 1.0, 8)
    glPopMatrix()
    
    # Derecho
    glPushMatrix()
    glTranslatef(1.2, 0.2, 0)
    glRotatef(-30, 0, 0, 1)
    draw_cylinder(0.2, 1.0, 8)
    glPopMatrix()
    
    # Piernas
    # Izquierda
    glPushMatrix()
    glTranslatef(-0.5, -2.0, 0)
    draw_cylinder(0.25, 0.8, 8)
    glPopMatrix()
    
    # Derecha
    glPushMatrix()
    glTranslatef(0.5, -2.0, 0)
    draw_cylinder(0.25, 0.8, 8)
    glPopMatrix()

def draw_sphere(radius, slices=16, stacks=16):
    """Dibuja esfera optimizada"""
    quad = gluNewQuadric()
    gluSphere(quad, radius, slices, stacks)
    gluDeleteQuadric(quad)

def draw_cylinder(radius, height, slices=16):
    """Dibuja cilindro optimizado"""
    quad = gluNewQuadric()
    gluCylinder(quad, radius, radius, height, slices, 1)
    gluDeleteQuadric(quad)

def draw_cone(radius, height, slices=16):
    """Dibuja cono para los cuernos"""
    quad = gluNewQuadric()
    gluCylinder(quad, radius, 0, height, slices, 1)
    gluDeleteQuadric(quad)

def setup_lighting():
    """Configura iluminación básica"""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    
    # Luz ambiental
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.4, 0.4, 0.4, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_POSITION, [2.0, 2.0, 2.0, 1.0])
    
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

def main():
    # Inicializar pygame
    pygame.init()
    
    # Configurar ventana
    width, height = 1000, 700
    screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Mike Wazowski - Control por Gestos")
    
    # Configurar OpenGL
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, width/height, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    
    # Configurar render
    glClearColor(0.1, 0.1, 0.3, 1.0)  # Fondo azul oscuro
    setup_lighting()
    
    # Crear controladores
    camera = Camera()
    hand_controller = HandGestureController()
    
    # Iniciar detección de gestos
    hand_controller.start_camera()
    
    clock = pygame.time.Clock()
    running = True
    rotation_angle = 0
    
    print("\n=== MIKE WAZOWSKI - CONTROL POR GESTOS ===")
    print("🖐️  Mano abierta: Controlar cámara")
    print("✊  Puño: Pausar")
    print("👍  Pulgar: Reset")
    print("ESC: Salir")
    print("Mira la ventana de cámara para ver la detección")
    
    while running:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Actualizar cámara
        camera.update_from_gesture(hand_controller)
        
        # Renderizar
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Aplicar cámara
        camera.apply()
        
        # Rotación automática lenta
        rotation_angle += 0.3
        glRotatef(rotation_angle, 0, 1, 0)
        
        # Dibujar Mike
        draw_mike_wazowski()
        
        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(60)
    
    # Cleanup
    hand_controller.camera_enabled = False
    pygame.quit()

if __name__ == "__main__":
    main()
```
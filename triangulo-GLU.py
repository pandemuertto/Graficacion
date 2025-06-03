# Este programa usa OpenGL con Python (PyOpenGL + GLUT) para renderizar una escena 3D básica. 
# En ella se dibuja un triángulo con colores RGB interpolados en un espacio tridimensional. 
# La escena se muestra dentro de una ventana con perspectiva 3D, 
# y se habilita la prueba de profundidad para futuros objetos tridimensionales.


import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Establecer color de fondo (negro)
    glEnable(GL_DEPTH_TEST)          # Habilitar prueba de profundidad
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 0.1, 50.0)  # Configuración de perspectiva
    glMatrixMode(GL_MODELVIEW)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpiar buffers
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5.0)  # Mover la cámara hacia atrás

    # Dibujar un triángulo
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)  # Rojo
    glVertex3f(-1.0, -1.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)  # Verde
    glVertex3f(1.0, -1.0, 0.0)
    glColor3f(0.0, 0.0, 1.0)  # Azul
    glVertex3f(0.0, 1.0, 0.0)
    glEnd()

    glutSwapBuffers()  # Intercambiar buffers (doble buffer)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    
    # IMPORTANTE: usar encode para evitar error por acentos
    glutCreateWindow("Triángulo con GLUT y Python".encode("utf-8"))

    init()
    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()

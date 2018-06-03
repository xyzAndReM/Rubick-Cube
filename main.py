import pygame
from pygame.locals import *
from quat import *
from geo import *
from cubinhos import *
from viewer import *
from controller import *
from OpenGL.GL import shaders
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np;

class cube():
    def __init__(self):
        self.controller = controller()
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    self.controller.handle_keydown(event.key)
                if event.type == pygame.KEYUP:
                    self.controller.handle_keyup(event.key)
            self.controller.update()

def main():
    cubo = cube();
    cubo.run();
main()
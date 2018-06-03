import pygame
from pygame.locals import *
from quat import *
from geo import *
from viewer import *

class controller:
    theta_inc = 5;
    theta = pi / 2 / theta_inc;
    def __init__(self):
        self.mode = 'x';
        self.level = 0
        self.viewer = viewer();
        self.selected = []
        self.select()
    def handle_keydown(self,key):
        if key == pygame.K_d:
            self.level += 1
            self.level = self.level % 3;
            self.select()
        if key == pygame.K_a:
            self.level -= 1
            if(self.level < 0 ):
                self.level = 2;
            self.select()
        if key == pygame.K_w:
            for i in range(theta_inc):
                for cubo in self.selected:
                    cubo.rotate(self.mode,-theta);
                self.viewer.update();
            rotateMatrix(self.mode,self.level)
        if key == pygame.K_r:
            self.viewer.ResetView()
        if key == pygame.K_UP:  # or event.key == pygame.K_w:
            self.viewer.inc_x = pi / 75
        if key == pygame.K_DOWN:  # or event.key == pygame.K_s:
            self.viewer.inc_x = -pi / 75
        if key == pygame.K_LEFT:  # or event.key == pygame.K_a:
            self.viewer.inc_y = pi / 75
        if key == pygame.K_RIGHT:  # or event.key == pygame.K_d:
             self.viewer.inc_y = -pi / 75
        if key == pygame.K_1:
            self.mode = 'x';
            self.select()
        if key == pygame.K_2:
            self.mode = 'y';
            self.select()
        if key == pygame.K_3:
            self.mode = 'z'
            self.select()
    def handle_keyup(self,key):
        if ( (key == pygame.K_UP) or (key == pygame.K_DOWN) or (key == pygame.K_w) or (key == pygame.K_s) ):
            self.viewer.inc_x = 0.0
        if ( (key == pygame.K_LEFT) or (key == pygame.K_RIGHT) or (key == pygame.K_a) or (key == pygame.K_d) or (key == pygame.K_l) or (key == pygame.K_f) ):
            self.viewer.inc_y = 0.0
    def select(self):
        while(self.selected):
            cubinho = self.selected.pop()
            cubinho.deselect();
        if(self.mode == 'x'):
            for i in range(3):
                for j in range(3):
                    cubinho = CuboMatriz[i][j][self.level]
                    cubinho.select()
                    self.selected.append(cubinho)
        elif(self.mode == 'y'):
            for i in range(3):
                for j in range(3):
                    cubinho = CuboMatriz[i][self.level][j]
                    cubinho.select()
                    self.selected.append(cubinho)
        elif(self.mode == 'z'):
            for i in range(3):
                for j in range(3):
                    cubinho = CuboMatriz[self.level][j][i]
                    cubinho.select()
                    self.selected.append(cubinho)
    def update(self):
        self.viewer.update();
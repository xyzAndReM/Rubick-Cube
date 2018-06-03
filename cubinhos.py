from geo import *
from quat import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np


def ThreeD(a, b, c):
    lst = [[ [ [] for col in range(a)] for col in range(b)] for row in range(c)]
    return lst
def rotateMatrix(mode,level):
    if(mode == 'x'):
        for i in range(3):
            for j in range(3):
                CuboMatrizAUX[i][j][level] = CuboMatriz[2-j][i][level]
        for i in range(3):
            for j in range(3):
                CuboMatriz[i][j][level] = CuboMatrizAUX[i][j][level]
    elif(mode =='y'):
        for i in range(3):
            for j in range(3):
                CuboMatrizAUX[i][level][j] = CuboMatriz[j][level][2-i]
        for i in range(3):
            for j in range(3):
                CuboMatriz[i][level][j] = CuboMatrizAUX[i][level][j]
    elif(mode =='z'):
        for i in range(3):
            for j in range(3):
                CuboMatrizAUX[level][i][j] = CuboMatriz[level][2-j][i]
        for i in range(3):
            for j in range(3):
                CuboMatriz[level][i][j] = CuboMatrizAUX[level][i][j]

    #printMatrix(mode,level)
theta_inc = 10;
theta = pi / 2 / theta_inc;

class cubinho:
    def __init__(self,center):
        self.center  = center #List of vertices
        self.orientation = (1.0,0.0,0.0,0.0)
        self.select_float = 0.0
    def select(self):
        self.select_float = 0.2
    def deselect(self):
        self.select_float = 0.0
    def rotate(self,mode,angle):
        if(mode == 'x'):
            self.center = x_rot(self.center,theta)
            rot = normalize(axisangle_to_q((1.0, 0.0, 0.0), -theta))
            self.orientation = q_mult(self.orientation, rot)
        elif(mode == 'y'):
            self.center = y_rot(self.center,theta)
            rot = normalize(axisangle_to_q((0.0, 1.0, 0.0), -theta))
            self.orientation = q_mult(self.orientation, rot)
        elif(mode == 'z'):
            self.center = z_rot(self.center,theta)
            rot = normalize(axisangle_to_q((0.0, 0.0, 1.0), -theta))
            self.orientation = q_mult(self.orientation, rot)

CuboMatriz = ThreeD(3,3,3);
CuboMatrizAUX = ThreeD(3,3,3);
cl = [-1.05,0.0,1.05];
for z in range(3):
    for y in range(3):
        for x in range(3):
            i,j,k = cl[x],cl[y],cl[z]
            CuboMatriz[z][y][x] = cubinho([i,j,k])


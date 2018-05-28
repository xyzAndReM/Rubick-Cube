from geo import *
from quat import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
ID = 0;
def printMatrix(mode,level):
    if(mode == 'x'):
        for i in range(3):
            print(CuboMatriz[0][i][level],CuboMatriz[1][i][level],CuboMatriz[2][i][level])
    print('\n');
def  print_vector(vector):
    string = ''
    for i in vector:
        string += (str(id(i)) + ' ')
    print(string)
    print('########################')


def ThreeD(a, b, c):
    lst = [[ [cubinho_vazio() for col in range(a)] for col in range(b)] for row in range(c)]
    return lst
def rotateMatrix(mode,level):
    printMatrix(mode,level)
    if(mode == 'x'):
        for i in range(3):
            for j in range(3):
                CuboMatrizAUX[i][j][level] = CuboMatriz[j][2-i][level]
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
                CuboMatrizAUX[level][i][j] = CuboMatriz[level][j][2-i]
        for i in range(3):
            for j in range(3):
                CuboMatriz[level][i][j] = CuboMatrizAUX[level][i][j]

    #printMatrix(mode,level)
theta_inc = 10;
theta = pi / 2 / theta_inc;


class cubinho_vazio:
    def draw(self):
        pass
    def select(self):
        pass
    def deselect(self):
        pass
    def rotate(self,mode):
        pass

class cubinho:
    ID = 0;
    def __init__(self,verts,paint_faces):
        global ID
        self.edge_color = (0.0,0.0,0.0);
        self.line_width = (0.4);
        self.verts = verts #List of vertices
        self.paint_faces = paint_faces
        self.paint_colors = paint_faces
        cubinho.ID += 1
        self.id = cubinho.ID
    def __str__(self):
        return (str(id(self))+ ' ')
    def draw(self):
        glLineWidth(GLfloat(6.0))
        glBegin(GL_LINES)
        glColor3fv(self.edge_color)
        for edge in cube_edges:
                for vertex in edge:
                    glVertex3fv(self.verts[vertex])
        glEnd()

        glBegin(GL_QUADS)
        for surface,color in zip(self.paint_faces,self.paint_colors):
            for vertex in cube_surfaces[surface]:
                glColor3fv(cube_colors[color])
                glVertex3fv(self.verts[vertex])
        glEnd()
    def select(self):
        self.edge_color = (0.4,0.0,0.6);
        self.line_width = (0.8)
    def deselect(self):
        self.edge_color = (0.0,0.0,0.0);
        self.line_width = (0.4)
    def rotate(self,mode):
        if(mode == 'x'):
            for i in range(8):
                self.verts[i] = x_rot(self.verts[i],theta)
        elif(mode == 'y'):
            for i in range(8):
                self.verts[i] = y_rot(self.verts[i],theta)
        elif(mode == 'z'):
            for i in range(8):
                self.verts[i] = z_rot(self.verts[i],theta) 



CuboMatriz = ThreeD(3,3,3);
CuboMatrizAUX = ThreeD(3,3,3);

#CUBOS CENTRAIS
CuboMatriz[2][1][1] = cubinho(center_pieces[0],[0])
CuboMatriz[1][1][0] = cubinho(center_pieces[1],[1])
CuboMatriz[0][1][1] = cubinho(center_pieces[2],[2])
CuboMatriz[1][1][2] = cubinho(center_pieces[3],[3])
CuboMatriz[1][0][1] = cubinho(center_pieces[4],[4])
CuboMatriz[1][2][1] = cubinho(center_pieces[5],[5])

#CUBOS NAS ARESTAS
#X
CuboMatriz[2][2][1] = cubinho(edge_pieces[0][0],[0,5])
CuboMatriz[2][0][1] = cubinho(edge_pieces[0][1],[0,4])
CuboMatriz[0][0][1] = cubinho(edge_pieces[0][2],[4,2])
CuboMatriz[0][2][1] = cubinho(edge_pieces[0][3],[2,5])

#Y
CuboMatriz[2][1][0] = cubinho(edge_pieces[1][0],[0,1])
CuboMatriz[0][1][0] = cubinho(edge_pieces[1][1],[1,2])
CuboMatriz[0][1][2] = cubinho(edge_pieces[1][2],[2,3])
CuboMatriz[2][1][2] = cubinho(edge_pieces[1][3],[3,0])

#Z
CuboMatriz[1][2][0] = cubinho(edge_pieces[2][0],[1,5])
CuboMatriz[1][0][0] = cubinho(edge_pieces[2][1],[1,4])
CuboMatriz[1][0][2] = cubinho(edge_pieces[2][2],[4,3])
CuboMatriz[1][2][2] = cubinho(edge_pieces[2][3],[3,5])

#CUBOS NAS PONTAS
#Front
CuboMatriz[2][2][0] = cubinho(corner_pieces[0],[1,0,5])
CuboMatriz[2][0][0] = cubinho(corner_pieces[1],[1,0,4])
CuboMatriz[2][0][2] = cubinho(corner_pieces[2],[4,0,3])
CuboMatriz[2][2][2] = cubinho(corner_pieces[3],[3,0,5])

#Back
CuboMatriz[0][2][0] = cubinho(corner_pieces[4],[1,2,5])
CuboMatriz[0][0][0] = cubinho(corner_pieces[5],[1,2,4])
CuboMatriz[0][0][2] = cubinho(corner_pieces[6],[4,2,3])
CuboMatriz[0][2][2] = cubinho(corner_pieces[7],[3,2,5])
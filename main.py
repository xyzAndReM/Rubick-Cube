import pygame
from pygame.locals import *
from quat import *
from geo import *
from cubinhos import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *

theta_inc = 10;
theta = pi / 2 / theta_inc;

def InitShader(rot_matrix):                # We call this right after our OpenGL window is created.  
    #glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
    #glClearDepth(1.0)                    # Enables Clearing Of The Depth Buffer
    glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading

    #glMatrixMode(GL_PROJECTION)
    #glLoadIdentity()                    # Reset The Projection Matrix
                                        # Calculate The Aspect Ratio Of The Window
    #gluPerspective(45.0, float(800)/float(600), 0.1, 100.0)

    #glMatrixMode(GL_MODELVIEW)
    #glLoadMatrixf(rot_matrix)

    if not glUseProgram:
        print('Missing Shader Objects!')
        sys.exit(1)

    global program
    program = compileProgram(
        compileShader('''
            // Application to vertex shader
            varying vec3 P;
            varying vec3 N;
            varying vec3 I;
            void main()
            {
                //Transform vertex by modelview and projection matrices
                gl_Position =  gl_ModelViewProjectionMatrix * gl_Vertex;
                // Position in clip space
                P = vec3( gl_ModelViewMatrix * gl_Vertex);
                // Normal transform (transposed model-view inverse)
                N = gl_NormalMatrix * gl_Normal;
                // Incident vector
                I = P;
                // Forward current color and texture coordinates after applying texture matrix
                gl_FrontColor = gl_Color;
                gl_TexCoord[0] = gl_TextureMatrix[0] * gl_MultiTexCoord0;
            }
        ''',GL_VERTEX_SHADER),
        compileShader('''
            varying vec3 P;
            varying vec3 N;
            varying vec3 I;
            uniform float edgefalloff;
            void main()
            {
                float opacity = dot(normalize(N), normalize(-I));
                opacity = abs(opacity);
                //opacity = 1.0 - pow(opacity, edgefalloff);
                gl_FragColor = opacity * gl_Color;
            }
    ''',GL_FRAGMENT_SHADER),
    )




class controller:
    def __init__(self):
        self.mode = 'x';
        self.level = 0
        self.inc_x = 0
        self.inc_y = 0
        self.accum = (1,0,0,0)
        self.zoom = 1
        self.selected = []
        self.select()

    def draw_cube(self):
        for colums in CuboMatriz:
            for colums in colums:
                for cubinhos in colums:
                    cubinhos.draw()

    def handle_keydown(self,key):
        if key == pygame.K_d:
            self.level += 1
            self.level = self.level % 3;
        if key == pygame.K_a:
            self.level -= 1
            if(self.level < 0 ):
                self.level = 2;
        if key == pygame.K_w:
            print_vector(self.selected)
            for i in range(theta_inc):
                for cubo in self.selected:
                    cubo.rotate(self.mode);
                self.update();
            rotateMatrix(self.mode,self.level)
        if key == pygame.K_UP:  # or event.key == pygame.K_w:
            self.inc_x = pi / 100
        if key == pygame.K_DOWN:  # or event.key == pygame.K_s:
            self.inc_x = -pi / 100
        if key == pygame.K_LEFT:  # or event.key == pygame.K_a:
            self.inc_y = pi / 100
        if key == pygame.K_RIGHT:  # or event.key == pygame.K_d:
            self.inc_y = -pi / 100
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
            self.inc_x = 0.0
        if ( (key == pygame.K_LEFT) or (key == pygame.K_RIGHT) or (key == pygame.K_a) or (key == pygame.K_d) or (key == pygame.K_l) or (key == pygame.K_f) ):
            self.inc_y = 0.0

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
        pygame.mouse.get_rel()  # prevents the cube from instantly rotating to a newly clicked mouse coordinate
        rot_x = normalize(axisangle_to_q((1.0, 0.0, 0.0), self.inc_x))
        rot_y = normalize(axisangle_to_q((0.0, 1.0, 0.0), self.inc_y))
            #nonlocal accum
        self.accum = q_mult(self.accum, rot_x)
        self.accum = q_mult(self.accum, rot_y)
        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(q_to_mat4(self.accum))
        InitShader(q_to_mat4(self.accum))
        glScalef(self.zoom, self.zoom, self.zoom)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.select()
        self.draw_cube()
        pygame.display.flip()



class cube():
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.controller = controller()
        pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption('PyCube')
        glClearColor(1, 1, 1, 0)
        # Using depth test to make sure closer colors are shown over further ones
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glutInit()
        # Default view
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.width / self.height), 0.5, 40)
        glTranslatef(0.0, 0.0, -17.5)
        InitShader(q_to_mat4(self.controller.accum))
        glUseProgram(program)
        #padding(0.3)
    def run(self):
        global moves
        pad_toggle = False
        mode = 1;
        select = {1:0 , 2:1}

        while True:
            theta_inc = 5;
            theta = pi / 2 / theta_inc;
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    self.controller.handle_keydown(event.key)
                if event.type == pygame.KEYUP:
                    self.controller.handle_keyup(event.key)

            #glRotatef(3, 1, 1, 1)
            self.controller.update()





def main():
    cubo = cube();
    cubo.run();


main()
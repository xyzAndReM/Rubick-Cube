import pygame
from pygame.locals import *
from quat import *
from geo import *
from cubinhos import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL import shaders
import numpy as np
from PIL import Image

X_Axis =pyrr.Vector3([1.0,0.0,0.0]);
Y_Axis = pyrr.Vector3([0.0,1.0,0.0]);
theta_inc = 10;
theta = pi / 2 / theta_inc;
VERTEX_SHADER = '''#version 330 core
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 texture;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 normal_matrix;

out vec3 vertex_normal;
out vec2 vertex_texture;
out vec3 FragPos;

void main()
{
    gl_Position = projection * view * model * vec4(position, 1.0f) ;
    FragPos = vec3(model * vec4(position, 1.0f));
    vertex_normal = mat3(view * model) * normal;
    vertex_texture = texture;
}'''

FRAGMENT_SHADER = '''#version 330 core
in vec3 vertex_normal;
in vec2 vertex_texture;
in vec3 FragPos;
uniform vec3 lightPos;
uniform float select_float;
out vec4 color;

uniform sampler2D cubo_tex;
uniform sampler2D select_tex;


void main()
{
    vec4 ambient = vec4(0.1,0.1,0.1,0.0);
    vec3 norm = normalize(vertex_normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float specularStrength = 0.75;
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(lightDir, reflectDir), 0.0), 128);
    vec4 specular = vec4( vec3(specularStrength * spec),1.0f) ;

    vec4 diffuse = vec4(diff,diff,diff,1.0f);
    color = (ambient + diffuse + specular)*mix( texture(cubo_tex, vertex_texture), texture(select_tex, vertex_texture),select_float) ;
}'''

def BuildShaderProgram():
        vertex_shader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
        fragment_shader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
        program = shaders.compileProgram(vertex_shader, fragment_shader)
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)
        return program;
def ReadVertexData():
        VERTEX_ID = glGenVertexArrays(1)
        # Conecta objeto vao
        glBindVertexArray(VERTEX_ID)
        # Cria um vertex buffer object
        vbo = glGenBuffers(1)
        # Conecta objeto vbo
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        # Copia os vetices em geo.py na memória
        glBufferData(GL_ARRAY_BUFFER, vertices.size * vertices.itemsize, vertices, GL_STATIC_DRAW)
        # Cria um element buffer object
        ebo = glGenBuffers(1)
        # Conecta objeto ebo
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        # Copia dados na memÃ³ria
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.size * indices.itemsize,indices, GL_STATIC_DRAW)
        
        # Especifica o local das coordenadas (posições) x, y, z
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize, None)
        glEnableVertexAttribArray(0)
        
        # Especifica o local das Normais
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize,
                              ctypes.c_void_p(3 * vertices.itemsize))
        glEnableVertexAttribArray(1)

        #Especifica o local das texturas
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 8 * vertices.itemsize,
                              ctypes.c_void_p(6 * vertices.itemsize))
        glEnableVertexAttribArray(2)
        
        # Desconecta vao
        glBindVertexArray(0)
        return VERTEX_ID;
def ReadTexture(filename,texture_number):
      # PIL can open BMP, EPS, FIG, IM, JPEG, MSP, PCX, PNG, PPM
      # and other file types.  We convert into a texture using GL.
      print('trying to open', filename)
      try:
         image = Image.open(filename)
      except IOError as ex:
         print('IOError: failed to open texture file')
         message = template.format(type(ex).__name__, ex.args)
         print(message)
         return -1
      print('opened file: size=', image.size, 'format=', image.format)
      imageData = numpy.array(list(image.getdata()), numpy.uint8)

      textureID = glGenTextures(1)
      glPixelStorei(GL_UNPACK_ALIGNMENT, 4)
      glActiveTexture(GL_TEXTURE0 + texture_number)
      glBindTexture(GL_TEXTURE_2D, textureID)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
      glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1],0, GL_RGB, GL_UNSIGNED_BYTE, imageData)
      glGenerateMipmap(GL_TEXTURE_2D);

      glBindVertexArray(0)
      image.close()
      return textureID
class viewer:
    def __init__(self):
        pygame.init()
        self.camera_pos = pyrr.Vector3([0.0,0.0,10.0])
        self.camera_up = (0.0,1.0,0.0);
        self.view = pyrr.Matrix44.look_at(self.camera_pos,(0,0,0),self.camera_up,dtype=np.float32)
        self.inc_x = 0
        self.inc_y = 0
        self.zoom = 1
        self.width = 800
        self.height = 600
        self.accum = (1,0,0,0)
        self.accum2 = (1,0,0,0)
        self.clock = pygame.time.Clock()

        pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption('PyCube')
        self.CubeShader = BuildShaderProgram()
        self.VAO = ReadVertexData();
        self.texture = ReadTexture('./textures/rubick3.png',0)
        self.selected_texture = ReadTexture('./textures/rubick7.png',1)
        # Cria matriz de projeçao
        projection = pyrr.Matrix44.perspective_projection(45.,self.width / self.height,.1,100.,dtype=np.float32)
        
        glUseProgram(self.CubeShader)
        # Retorna a localização das variÃ¡veis uniformes
        self.model_loc = glGetUniformLocation(self.CubeShader, 'model')
        self.view_loc = glGetUniformLocation(self.CubeShader, 'view')
        self.light_loc = glGetUniformLocation(self.CubeShader,'lightPos')
        self.normal_loc = glGetUniformLocation(self.CubeShader,'normal_matrix')
        self.select_loc = glGetUniformLocation(self.CubeShader, 'select_float')
        proj_loc = glGetUniformLocation(self.CubeShader, 'projection')
        # Define o valor da variÃ¡vel uniforme `projection`gg
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        glUniform1i(glGetUniformLocation(self.CubeShader, "cubo_tex"), 0);
        glUniform1i(glGetUniformLocation(self.CubeShader, "select_tex"), 1);
        glUseProgram(0)
        # Teste de profundidade (utilizar em 3D)
        glEnable(GL_DEPTH_TEST)
        glClearColor(1, 1, 1, 0)
    def ViewMatrix(self):
        rot_x = normalize(axisangle_to_q((1.0, 0.0, 0.0), self.inc_x))
        rot_y = normalize(axisangle_to_q((0.0, 1.0, 0.0), self.inc_y))
        rot_total = q_mult(rot_x,rot_y);
        self.accum = q_mult(self.accum, rot_total)
        VIEW = pyrr.matrix44.multiply(q_to_mat4(self.accum),self.view)
        glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, VIEW)
        glUniform3fv(self.light_loc, 1, self.camera_pos)
        return VIEW;
    def ResetView(self):
        self.accum = (1.0,0.0,0.0,0.0);
    def ModelMatrix(self):
        for rows in CuboMatriz:
            for colums  in rows:
                for cubinho in colums:
                    TRANSLATION = pyrr.Matrix44.from_translation(cubinho.center, dtype=np.float16)
                    MODEL = pyrr.matrix44.multiply(q_to_mat4(cubinho.orientation),TRANSLATION)
                    glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, MODEL)
                    glActiveTexture(GL_TEXTURE1);
                    glBindTexture(GL_TEXTURE_2D,self.selected_texture)
                    glActiveTexture(GL_TEXTURE0);
                    glBindTexture(GL_TEXTURE_2D, self.texture);
                    glUniform1f(self.select_loc,cubinho.select_float)
                    glDrawElements(GL_TRIANGLES, indices.size, GL_UNSIGNED_BYTE, None)

    def update(self):
        pygame.mouse.get_rel()  # prevents the cube from instantly rotating to a newly clicked mouse coordinate
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.CubeShader)
        glBindVertexArray(self.VAO)

        self.ViewMatrix()
        self.ModelMatrix()
        glBindVertexArray(0)
        glUseProgram(0)
        
        pygame.display.flip()
        self.clock.tick(40)

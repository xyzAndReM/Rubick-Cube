import numpy as np
import pyrr

        
vertices = np.array([
                             # Frente          Normals            Texttures
                             -0.5,  0.5,  0.5, 0.0, 0.0, 1.0,   0.0, 1.0,
                              0.5,  0.5,  0.5, 0.0, 0.0, 1.0,   1/3, 1.0,
                             -0.5, -0.5,  0.5, 0.0, 0.0, 1.0,  0.0, 2/3,
                              0.5, -0.5,  0.5, 0.0, 0.0, 1.0,  1/3, 2/3,
                             
                             # Fundo           Cores
                             -0.5,  0.5, -0.5, 0.0, 0.0, -1.0, 1/3, 1.0,
                              0.5,  0.5, -0.5, 0.0, 0.0, -1.0, 2/3, 1.0,
                             -0.5, -0.5, -0.5, 0.0, 0.0, -1.0, 1/3, 2/3,
                              0.5, -0.5, -0.5, 0.0, 0.0, -1.0, 2/3, 2/3,
                              
                             # Esquerda        Cores
                             -0.5,  0.5,  0.5, -1.0, 0.0, 0.0, 2/3, 1.0,
                             -0.5,  0.5, -0.5, -1.0, 0.0, 0.0, 1.0, 1.0,
                             -0.5, -0.5,  0.5, -1.0, 0.0, 0.0, 2/3, 2/3,
                             -0.5, -0.5, -0.5, -1.0, 0.0, 0.0, 1.0, 2/3,
                              
                             # Direita         Cores
                              0.5,  0.5,  0.5, 1.0, 0.0, 0.0, 0.0, 2/3,
                              0.5,  0.5, -0.5, 1.0, 0.0, 0.0, 1/3, 2/3,
                              0.5, -0.5,  0.5, 1.0, 0.0, 0.0, 0.0, 1/3,
                              0.5, -0.5, -0.5, 1.0, 0.0, 0.0, 1/3, 1/3,
                             
                             # Topo            Cores
                             -0.5,  0.5, -0.5, 0.0, 1.0, 0.0, 1/3, 2/3,
                              0.5,  0.5, -0.5, 0.0, 1.0, 0.0, 2/3, 2/3,
                             -0.5,  0.5,  0.5, 0.0, 1.0, 0.0, 1/3, 1/3,
                              0.5,  0.5,  0.5, 0.0, 1.0, 0.0, 2/3, 1/3,
                             
                             # Base            Cores
                             -0.5, -0.5, -0.5, 0.0, -1.0, 0.0, 2/3, 2/3,
                              0.5, -0.5, -0.5, 0.0, -1.0, 0.0, 1.0, 2/3,
                             -0.5, -0.5,  0.5, 0.0, -1.0, 0.0, 2/3, 1/3,
                              0.5, -0.5,  0.5, 0.0, -1.0, 0.0, 1.0, 1/3
                            ], dtype=np.float32)

indices = np.array([
                                 0,  1,  2,  1,  2,  3,
                                 4,  5,  6,  5,  6,  7,
                                 8,  9, 10,  9, 10, 11,
                                12, 13, 14, 13, 14, 15,
                                16, 17, 18, 17, 18, 19,
                                20, 21, 22, 21, 22, 23 
                               ], dtype=np.uint8)

#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import numpy as np
from tool import create_program_from_file
import pyrr

class Game(object):
    """ fenêtre GLFW avec openGL """

    def __init__(self):
        self.x = 0
        self.y = 0
        self.r = 0
        self.window = self.init_window()
        self.init_context()
        self.init_programs()
        self.init_data()


    def init_window(self):
        # initialisation de la librairie glfw et du context opengl associé
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et parametrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        window = glfw.create_window(800, 800, 'OpenGL', None, None)
        # parametrage de la fonction de gestion des évènements
        glfw.set_key_callback(window, self.key_callback)
        return window

    def init_context(self):
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)

    def init_programs(self):
        GL.glUseProgram(create_program_from_file("shader.vert","shader.frag"))

        
    def init_data(self):
        sommets = np.array(((0, 0, 0), (1, 0, 0), (0, 1, 0)), np.float32)
        # attribution d'une liste d'´etat (1 indique la cr´eation d'une seule liste)
        vao = GL.glGenVertexArrays(1)
        # affectation de la liste d'´etat courante
        GL.glBindVertexArray(vao)
        # attribution d’un buffer de donn´ees (1 indique la cr´eation d’un seul buffer)
        vbo = GL.glGenBuffers(1)
        # affectation du buffer courant
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        # copie des donnees des sommets sur la carte graphique
        GL.glBufferData(GL.GL_ARRAY_BUFFER, sommets, GL.GL_STATIC_DRAW)
        # Les deux commandes suivantes sont stock´ees dans l'´etat du vao courant
        # Active l'utilisation des donn´ees de positions
        # (le 0 correspond `a la location dans le vertex shader)
        GL.glEnableVertexAttribArray(0)
        # Indique comment le buffer courant (dernier vbo "bind´e")
        # est utilis´e pour les positions des sommets
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)


    def run(self):
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # choix de la couleur de fondglClear
            GL.glClearColor(0.5, 0.6, 0.9, 1.0)
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)


            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()

            
    
    def key_callback(self, win, key, scancode, action, mods):

        prog = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM)
        loc = GL.glGetUniformLocation(prog, "translation")
        loc2 = GL.glGetUniformLocation(prog, "rotation")

        color = GL.glGetUniformLocation(prog, "color1")
       
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)
        
        if key == glfw.KEY_R and action == glfw.PRESS:
            GL.glUniform4f(color, 1, 0,0, 0)
        
        if key == glfw.KEY_G and action == glfw.PRESS:
            GL.glUniform4f(color, 0, 1,0, 0)

        if key == glfw.KEY_B and action == glfw.PRESS:
            GL.glUniform4f(color, 0, 0,1,0)
        
        if key == glfw.KEY_Z and glfw.get_key(win, glfw.KEY_Z)  == glfw.PRESS:
            GL.glUniform4f(loc, self.x, self.y+0.01,0, 0)
            self.y+=0.01
        
        if key == glfw.KEY_Q and glfw.get_key(win, glfw.KEY_Q) == glfw.PRESS:
            GL.glUniform4f(loc, self.x-0.01, self.y,0, 0)
            self.x-=0.01

        if key == glfw.KEY_S and glfw.get_key(win, glfw.KEY_S) == glfw.PRESS:
            GL.glUniform4f(loc, self.x, self.y-0.01,0, 0)
            self.y-=0.01

        if key == glfw.KEY_D and glfw.get_key(win, glfw.KEY_D) == glfw.PRESS:
            GL.glUniform4f(loc, self.x+0.01, self.y,0, 0)
            self.x+=0.01
        
        if key == glfw.KEY_I and glfw.get_key(win, glfw.KEY_I)  == glfw.PRESS:
            rot3 = pyrr.matrix33.create_from_z_rotation(np.pi*self.r/200)
            rot4 = pyrr.matrix44.create_from_matrix33(rot3)
            GL.glUniformMatrix4fv(loc2, 1, GL.GL_FALSE, rot4)
            self.r += 1

def main():
    g = Game()
    g.run()
    glfw.terminate()

if __name__ == '__main__':
    main()
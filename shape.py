##shape.py: High level graphics shaspes such squares, circles, whatever
##Copyright (C) 2017  Oscar Triano 'dotoscat'
##
##This program is free software: you can redistribute it and/or modify
##it under the terms of the GNU General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU General Public License for more details.
##
##You should have received a copy of the GNU General Public License
##along with this program.  If not, see <http://www.gnu.org/licenses/>.

from math import sqrt, fabs, sin
from pyglet.gl import *
import pyglet.graphics

class Square(object):
    def __init__(self, width, height):
        HALF_WIDTH = width/2
        HALF_HEIGHT = height/2
        TOP_LEFT = (-HALF_WIDTH, HALF_HEIGHT)
        TOP_RIGHT = (HALF_WIDTH, HALF_HEIGHT)
        BOTTOM_LEFT = (-HALF_WIDTH, -HALF_HEIGHT)
        BOTTOM_RIGHT = (HALF_WIDTH, -HALF_HEIGHT)
        RED = (1., 0., 0.)
        GREEN = (0., 1., 0.)
        BLUE = (0., 0., 1.)
        WHITE = (1., 1., 1.)
        self.vertex_list = pyglet.graphics.vertex_list(4,
            ('v2f', (*TOP_LEFT, *TOP_RIGHT, *BOTTOM_RIGHT, *BOTTOM_LEFT)),
            ('c3f', (*RED, *GREEN, *BLUE, *WHITE))
        )
        self.old_x = 0.
        self.old_y = 0.
        self.x = 0.
        self.y = 0.
        self.vel_x = 0.
        self.vel_y = 0.
        self.rotation = 0.
        self.rotation_speed = 0.
        self.radius = HALF_WIDTH
        self.time = 0.0

    def collides_with(self, square):
        distance = sqrt((self.x - square.x)**2 + (self.y - square.y)**2)
        return distance < self.radius + square.radius

    def apply_force(self, x, y, dt):
        self.vel_x += x*dt
        self.vel_y += y*dt

    def move(self, dx=0., dy=0.):
        self.x += dx
        self.y += dy

    def get_dx(self):
        return self.x - self.old_x

    def get_dy(self):
        return self.y - self.old_y

    def set_position(self, x, y):
        self.set_position_x(x)
        self.set_position_y(y)

    def set_position_y(self, y):
        self.old_y = self.y
        self.y = y

    def set_position_x(self, x):
        self.old_x = self.x
        self.x = x

    def get_position_y(self):
        return self.y

    def rotate(self, ddegrees):
        self.degrees += ddegrees

    def set_rotation(self, rotation):
        self.rotation = rotation

    def set_rotation_speed(self, speed):
        self.rotation_speed = speed

    def get_speed_x(self):
        return self.vel_x

    def set_speed_x(self, vel_x):
        self.vel_x = vel_x

    def set_speed_y(self, vel_y):
        self.vel_y = vel_y
    
    def update(self, dt):
        self.old_x = self.x
        self.old_y = self.y
        self.x += self.vel_x*dt
        self.y += self.vel_y*dt
        self.rotation += self.rotation_speed*dt
        self.time += dt

    def apply_sin(self, amplitude, base_y):
        self.old_y = self.y
        y = sin(self.time)*amplitude
        self.y = base_y + y

    def push_shape(self, square, G, dt):
        distance = sqrt((self.x - square.x)**2 + (self.y - square.y)**2)
        force = G/distance**2
        square.apply_force(0., force, dt)
    
    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(self.x, self.y, 0.)
        glRotatef(self.rotation, 0., 0., 1.)
        self.vertex_list.draw(GL_QUADS)

    def is_out(self, bound=0.):
        return self.x <= bound

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
        self.x = 0.
        self.y = 0.
        self.vel_x = 0.
        self.vel_y = 0.
        self.rotation = 0.
        self.rotation_speed = 0.

    def move(self, dx=0., dy=0.):
        self.x += dx
        self.y += dy

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def rotate(self, ddegrees):
        self.degrees += ddegrees

    def set_rotation(self, degrees):
        self.degrees = degrees

    def set_speed(self, vel_x, vel_y):
        self.vel_x = vel_x
        self_vel_y = vel_y
    
    def update(self, dt):
        self.x += self.vel_x*dt
        self.y += self.vel_y*dt
    
    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(self.x, self.y, 0.)
        glRotatef(self.degrees, 0., 0., 1.)
        self.vertex_list.draw(GL_QUADS)
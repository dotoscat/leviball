#!/usr/bin/env python
from pyglet.gl import *

def main():
    import pyglet
    import shape
    window = pyglet.window.Window()
    label = pyglet.text.Label('Hello world!',
                              font_name='Impact',
                              font_size=24,
                              x=window.width//2, y=window.height//2,
                              anchor_x='center', anchor_y='center')
    square = shape.Square(32, 32)
    square.set_position(200, 200)
    square.set_rotation_speed(77)
    
    @window.event
    def on_draw():
        window.clear()
        square.draw()
        glLoadIdentity()
        label.draw()
    
    def update(dt):
        square.update(dt)

    pyglet.clock.schedule_interval(update, 1./60.)
    
    pyglet.app.run()

if __name__ == '__main__':
    main()

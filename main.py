#!/usr/bin/env python
from pyglet.gl import *

def main():
    import pyglet
    import shape
    import random
    WIDTH = 800
    HEIGHT = 600
    OBSTACLE_SIZE = 4
    window = pyglet.window.Window(WIDTH, HEIGHT)
    label = pyglet.text.Label('Hello world!',
                              font_name='Impact',
                              font_size=24,
                              x=window.width//2, y=window.height//2,
                              anchor_x='center', anchor_y='center')
    square = shape.Square(32, 32)
    square.set_position(200, 200)
    square.set_rotation_speed(77)

    obstacles = [shape.Square(OBSTACLE_SIZE, OBSTACLE_SIZE) for i in range(4)]
    used_obstacles = []

    def generate_obstacle():
        if not obstacles: return
        obstacle = obstacles.pop()
        obstacle.set_position(WIDTH+OBSTACLE_SIZE, random.randint(0, HEIGHT//2))
        obstacle.set_speed(-random.randint(32, 64), 0.)
        obstacle.set_rotation_speed(random.randint(8, 128))
        used_obstacles.append(obstacle)
        
    @window.event
    def on_draw():
        window.clear()
        square.draw()
        for obstacle in used_obstacles: obstacle.draw()
        glLoadIdentity()
        label.draw()
    
    def update(dt):
        square.update(dt)
        generate_obstacle()
        for obstacle in used_obstacles: obstacle.update(dt)

    pyglet.clock.schedule_interval(update, 1./60.)
    
    pyglet.app.run()

if __name__ == '__main__':
    main()

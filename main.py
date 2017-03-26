#!/usr/bin/env python
import random
import pyglet
from pyglet.gl import *
import shape

def main():
    WIDTH = 800
    HEIGHT = 600
    OBSTACLE_SIZE = 4
    window = pyglet.window.Window(WIDTH, HEIGHT)
    label = pyglet.text.Label('Hello world!',
                              font_name='Impact',
                              font_size=24,
                              x=window.width//2, y=window.height//2,
                              anchor_x='center', anchor_y='center')
    base = shape.Square(32, 32)
    base.set_position(200, 0+16)
    
    square = shape.Square(32, 32)
    square.set_position(200, 200)
    square.set_rotation_speed(77)

    obstacles = [shape.Square(OBSTACLE_SIZE, OBSTACLE_SIZE) for i in range(4)]
    used_obstacles = []

    GAME_OVER = 0
    RUNNING = 1
    PAUSED = 2

    status = GAME_OVER

    def generate_obstacle():
        if not obstacles: return
        obstacle = obstacles.pop()
        obstacle.set_position(WIDTH+OBSTACLE_SIZE, random.randint(0, HEIGHT//2))
        obstacle.set_speed(-random.randint(32, 64), 0.)
        obstacle.set_rotation_speed(random.randint(8, 128))
        used_obstacles.append(obstacle)

    def recycle_obstacle():
        if not used_obstacles: return
        i = 0
        while i < len(used_obstacles):
            if used_obstacles[i].is_out():
                obstacles.append(used_obstacles.pop(i))
            else:
                i += 1

    def check_collision():
        for obstacle in used_obstacles:
            if square.collides_with(obstacle):
                return True
        return False

    def gravity(self):
        pass
    
    @window.event
    def on_draw():
        window.clear()
        base.draw()
        square.draw()
        for obstacle in used_obstacles: obstacle.draw()
        glLoadIdentity()
        label.draw()

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        base.move(dx=dx)
        square.move(dx=dx)
        if base.x < 0.:
            base.x = 0.
        if base.x > WIDTH:
            base.x = WIDTH
            
        if square.x < 0.:
            square.x = 0.
        if square.x > WIDTH:
            square.x = WIDTH

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        print('Jump!')
    
    def update(dt):
        base.update(dt)
        square.apply_force(0., -64., dt)#gravity
        square.apply_force(0., 32., dt)
        square.update(dt)
        for obstacle in used_obstacles: obstacle.update(dt)
        generate_obstacle()
        recycle_obstacle()
        if check_collision():
            print('Game over!')

    pyglet.clock.schedule_interval(update, 1./60.)
    
    pyglet.app.run()

if __name__ == '__main__':
    main()

#!/usr/bin/env python
import random
import pyglet
from pyglet.gl import *
import pyglet.window.key as key
import shape
from game_data import GameData

VERSION="1.0b"

MAIN_SCREEN ="""
LEVIBALL {}

Oscar Triano 'dotoscat' @cat_dotoscat

Use your mouse to avoid small things. Do click to jump.
In game press any key to pause the game.

Press any key to start the game.
    
""".format(VERSION)

def main():
    WIDTH = 800
    HEIGHT = 600
    OBSTACLE_SIZE = 4
    window = pyglet.window.Window(WIDTH, HEIGHT)
    paused_label = pyglet.text.Label('PAUSED',
                              font_name='Impact',
                              font_size=24,
                              x=window.width//2, y=window.height//2,
                              anchor_x='center', anchor_y='center')
    meters_label = pyglet.text.Label('',
                              font_name='Impact',
                              font_size=24,
                              x=window.width//2, y=window.height-24,
                              anchor_x='center', anchor_y='center')
    intro_label = pyglet.text.Label(MAIN_SCREEN,
                              font_name='Impact',
                              font_size=24,
                              x=window.width//2, y=window.height//2,
                              anchor_x='center', anchor_y='center',
                              multiline=True, width=WIDTH//2)
    base = shape.Square(32, 32)
    base.set_position(0, 0-0+16-0)
    
    square = shape.Square(32, 32)
    square.set_position(0, HEIGHT/4.0)
    square.set_rotation_speed(77)

    obstacles = [shape.Square(OBSTACLE_SIZE, OBSTACLE_SIZE) for i in range(4)]
    used_obstacles = []

    game_data = GameData()

    game_data.set_running()

    def update(dt):
        if game_data.is_paused(): return
        if game_data.is_running(): game_data.update(dt)
        meters_label.text = 'Meters {}'.format(game_data.get_meters())
        square.update(dt)
        base.set_rotation_speed(game_data.get_speed()*-256.)
        base.apply_force(0., -HEIGHT*2., dt)#gravity
        base.update(dt)
        if base.y < 16.:
            base.set_position_y(16.)
            base.set_speed(0., 0.)
        square.apply_sin(HEIGHT/8.0, base.get_position_y()+128.0)
        for obstacle in used_obstacles: obstacle.update(dt)
        if game_data.is_running():
            generate_obstacle()
            recycle_obstacle()
        if check_collision():
            print('Game over!')

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
            if base.collides_with(obstacle):
                return True
        return False
    
    @window.event
    def on_draw():
        window.clear()
        base.draw()
        square.draw()
        for obstacle in used_obstacles: obstacle.draw()
        glLoadIdentity()
        meters_label.draw()
        if game_data.is_paused(): paused_label.draw()
        elif game_data.is_over(): intro_label.draw() 

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        if game_data.is_paused(): return
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
        if game_data.is_paused(): return
        if base.y == 16.:
            base.set_speed(0., HEIGHT/1.5)

    @window.event
    def on_key_press(symbol, modifiers):
        if game_data.is_over():
            game_data.set_running()
        elif game_data.is_running():
            game_data.set_paused()
        elif game_data.is_paused():
            game_data.set_running()
    
    pyglet.clock.schedule_interval(update, 1./60.)
    
    pyglet.app.run()

if __name__ == '__main__':
    main()

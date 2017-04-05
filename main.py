#!/usr/bin/env python

##main.py: here is where the game starts and a minimal engine
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

import random
import pyglet
from pyglet.gl import *
from pyglet.window import key
import shape
from game_data import GameData
from player import Player

VERSION="0.10b"

MAIN_SCREEN ="""
LEVIBALL {}

Oscar Triano 'dotoscat' @cat_dotoscat

Arrow keys to move. Space to pause the game. 

Press space to start the game.
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
    gameover_label = pyglet.text.Label('GAME OVER\nPress \'space\' to try again',
                              font_name='Impact',
                              font_size=24,
                              x=window.width//2, y=window.height//2,
                              anchor_x='center', anchor_y='center',
                              multiline=True, width=WIDTH//2)

    player = Player(HEIGHT/4.0, HEIGHT/8.0)
    player.set_position_x(WIDTH/2.0)

    OBSTACLES = 8

    obstacles = [shape.Square(OBSTACLE_SIZE, OBSTACLE_SIZE) for i in range(OBSTACLES)]
    used_obstacles = []

    game_data = GameData(WIDTH)

    def reset_game():
        player.set_position_x(WIDTH/2.0)
        player.move(0.)
        game_data.reset()
        while len(used_obstacles):
            obstacles.append(used_obstacles.pop())

    def update(dt):
        if game_data.is_paused(): return
        if not game_data.is_over(): player.update(dt, -HEIGHT*2., HEIGHT/8.0)
        if game_data.is_running():
            game_data.update(dt)
            if game_data.new_advance() and random.randint(0, 1):
                generate_obstacle()
            recycle_obstacle()
            for obstacle in used_obstacles:
                obstacle.set_speed_x(game_data.get_speed()*-64.)
                obstacle.update(dt)
        if player.check_collision(used_obstacles):
            game_data.set_over()
            player.move(0.)
        player.fix_position(WIDTH)
        meters_label.text = 'Meters {}'.format(game_data.get_meters())

    def generate_obstacle():
        if not obstacles: return
        obstacle = obstacles.pop()
        y = random.randint(0, 128+64)
        generate_obstacle_for_base = True
        for used_obstacle in used_obstacles:
            if used_obstacle.get_position_y() < 64.0:
                generate_obstacle_for_base = False
                break
        if generate_obstacle_for_base:
            y = random.randint(0, 64)
        else:
            y = random.randint(0, 128+64)
        obstacle.set_position(WIDTH+OBSTACLE_SIZE, y)
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

    @window.event
    def on_draw():
        window.clear()
        player.draw()
        for obstacle in used_obstacles: obstacle.draw()
        glLoadIdentity()
        if not game_data.is_main_screen(): meters_label.draw()
        if game_data.is_paused(): paused_label.draw()
        elif game_data.is_over(): gameover_label.draw()
        elif game_data.is_main_screen(): intro_label.draw()

    @window.event
    def on_key_press(symbol, modifiers):
        jump = symbol == key.UP
        move_left = symbol == key.LEFT
        move_right = symbol == key.RIGHT
        space = symbol == key.SPACE
        if jump and not game_data.is_paused() and not game_data.is_over():
            player.jump(HEIGHT/1.5)
        if move_left and not game_data.is_over():
            player.move(-WIDTH/2.)
        elif move_right and not game_data.is_over():
            player.move(WIDTH/2.)
        if space and game_data.is_running():
            game_data.set_paused()
        elif space and game_data.is_paused():
            game_data.set_running()
        if space and (game_data.is_over() or game_data.is_main_screen()):
            reset_game()
        if symbol == key.F1:
            pyglet.image.get_buffer_manager().\
            get_color_buffer().save('screenshot.png')

    @window.event
    def on_key_release(symbol, modifiers):
        left = symbol == key.LEFT
        right = symbol == key.RIGHT
        if left and player.is_moving_left():
            player.move(0.)
        if right and player.is_moving_right():
            player.move(0.)
            

    pyglet.clock.schedule_interval(update, 1./60.)
    
    pyglet.app.run()

if __name__ == '__main__':
    main()

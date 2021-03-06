##player.py: Makes easy player movement, collision and so
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

import shape

class Player(object):
    def __init__(self, ball_position, amplitude):
        self.AMPLITUDE = amplitude
        self.base = shape.Square(32, 32)
        self.base.set_position(0, 0-0+16-0)
        self.ball = shape.Square(32, 32)
        self.ball.set_position(0, ball_position)
        self.ball.set_rotation_speed(77)

    def update(self, dt, g_force, speed):
        base = self.base
        ball = self.ball

        ball.update(dt)
        base.set_rotation_speed(speed)
        base.apply_force(0., g_force, dt)
        base.update(dt)
        if base.y < 16.:
            base.set_position_y(16.)
            base.set_speed_y(0.)
        ball.apply_sin(self.AMPLITUDE, base.get_position_y()+128.0)

    def check_collision(self, obstacles):
        base = self.base
        ball = self.ball
        
        for obstacle in obstacles:
            if base.collides_with(obstacle):
                return True
            if ball.collides_with(obstacle):
                return True
        return False

    def fix_position(self, width):
        base = self.base
        ball = self.ball
        
        if base.x < 0.:
            base.x = 0.
        if base.x > width:
            base.x = width
            
        if ball.x < 0.:
            ball.x = 0.
        if ball.x > width:
            ball.x = width

    def set_position_x(self, pos_x):
        self.base.set_position_x(pos_x)
        self.ball.set_position_x(pos_x)

    def move(self, vel_x):
        self.base.set_speed_x(vel_x)
        self.ball.set_speed_x(vel_x)

    def jump(self, speed):
        if self.base.get_position_y() == 16.:
            self.base.set_speed_y(speed)

    def draw(self):
        self.base.draw()
        self.ball.draw()
        
    def is_moving_left(self):
        return self.base.get_speed_x() < 0.0

    def is_moving_right(self):
        return self.base.get_speed_x() > 0.0

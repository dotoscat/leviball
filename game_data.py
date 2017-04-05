##game_data.py: Manages game status
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

class GameData(object):
    GAME_OVER = 0
    RUNNING = 1
    PAUSED = 2
    MAIN_SCREEN = 3
    def __init__(self, max_speed):
        self.MAX_SPEED = max_speed
        self.reset()
        self.set_main()

    def update(self, dt):
        self.secs += dt*self.speed
        self.space = False
        if self.secs > 1.0:
            self.secs = 0.0
            self.speed += 0.01
            if self.speed > self.MAX_SPEED:
                self.speed = self.MAX_SPEED
            self.meters += 1
            if self.meters > self.last_meters + 1 + self.speed:
                self.last_meters = self.meters
                self.space = True

    def get_speed(self):
        return self.speed

    def get_meters(self):
        return self.meters

    def new_advance(self):
        return self.space

    def is_running(self):
        return self.status == GameData.RUNNING

    def is_paused(self):
        return self.status == GameData.PAUSED

    def is_over(self):
        return self.status == GameData.GAME_OVER

    def is_main_screen(self):
        return self.status == GameData.MAIN_SCREEN

    def set_running(self):
        self.status = GameData.RUNNING

    def set_paused(self):
        self.status = GameData.PAUSED

    def set_over(self):
        self.status = GameData.GAME_OVER

    def set_main(self):
        self.status = GameData.MAIN_SCREEN

    def reset(self):
        self.new_space = False
        self.last_meters = 0
        self.speed = 1.
        self.meters = 0
        self.secs = 0.
        self.set_running()

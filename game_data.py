class GameData(object):
    GAME_OVER = 0
    RUNNING = 1
    PAUSED = 2
    def __init__(self):
        self.reset()

    def update(self, dt):
        self.secs += dt*self.speed
        if self.secs > 1.0:
            self.secs = 0.0
            self.speed += 0.01
            self.meters += 1

    def get_speed(self):
        return self.speed

    def get_meters(self):
        return self.meters

    def is_running(self):
        return self.status == GameData.RUNNING

    def is_paused(self):
        return self.status == GameData.PAUSED

    def is_over(self):
        return self.status == GameData.GAME_OVER

    def set_running(self):
        self.status = GameData.RUNNING

    def set_paused(self):
        self.status = GameData.PAUSED

    def set_over(self):
        self.status = GameData.GAME_OVER

    def reset(self):
        self.speed = 1.
        self.meters = 0
        self.secs = 0.
        self.set_over()

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

    def move(self, vel_x):
        self.base.set_speed_x(vel_x)
        self.ball.set_speed_x(vel_x)

    def jump(self, speed):
        if self.base.get_position_y() == 16.:
            self.base.set_speed_y(speed)

    def draw(self):
        self.base.draw()
        self.ball.draw()
        

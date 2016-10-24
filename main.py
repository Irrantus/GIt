import random

from kivy.app import App
from kivy.properties import NumericProperty, ReferenceListProperty, Clock, ObjectProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    f = 1
    f1 = 1
    f2 = 1
    f3 = 1
    i = 0
    j = 1
    k = 2
    steps = [0.001, 0.0025, 0.005]

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel
        self.ball.size[0] = 50
        self.ball.size[1] = 50
        self.f = 1

    def update_size(self):
        if self.ball.size[0] == 200:
            self.f = 0
            self.ball.size[0] -= 0.125
            self.ball.size[1] -= 0.125
        elif self.ball.size[0] == 10:
            self.f = 1
            self.ball.size[0] += 0.125
            self.ball.size[1] += 0.125
        elif self.ball.size[0] < 200 and self.f == 1:
            self.ball.size[0] += 0.125
            self.ball.size[1] += 0.125
        elif self.ball.size[0] > 10 and self.f == 0:
            self.ball.size[0] -= 0.125
            self.ball.size[1] -= 0.125

    def update_color(self):
        if self.ball.r == 1:
            self.f1 = 0
            self.i = random.choice(self.steps)
            self.ball.r = round(self.ball.r - self.i, 4)
        elif self.ball.r == 0:
            self.f1 = 1
            self.i = random.choice(self.steps)
            self.ball.r = round(self.ball.r + self.i, 4)
        elif self.ball.r < 1 and self.f1 == 1:
            self.ball.r = round(self.ball.r + self.i, 4)
        elif self.ball.r > 0 and self.f1 == 0:
            self.ball.r = round(self.ball.r - self.i, 4)

        if self.ball.g == 1:
            self.f2 = 0
            self.j = random.choice(self.steps)
            self.ball.g = round(self.ball.g - self.j, 4)
        elif self.ball.g == 0:
            self.f2 = 1
            self.j = random.choice(self.steps)
            self.ball.g = round(self.ball.g + self.j, 4)
        elif self.ball.g < 1 and self.f2 == 1:
            self.ball.g = round(self.ball.g + self.j, 4)
        elif self.ball.g > 0 and self.f2 == 0:
            self.ball.g = round(self.ball.g - self.j, 4)

        if self.ball.b == 1:
            self.f3 = 0
            self.k = random.choice(self.steps)
            self.ball.b = round(self.ball.b - self.k, 4)
        elif self.ball.b == 0:
            self.f3 = 1
            self.k = random.choice(self.steps)
            self.ball.b = round(self.ball.b + self.k, 4)
        elif self.ball.b < 1 and self.f3 == 1:
            self.ball.b = round(self.ball.b + self.k, 4)
        elif self.ball.b > 0 and self.f3 == 0:
            self.ball.b = round(self.ball.b - self.k, 4)

        if round(self.ball.r, 1) == 1 and round(self.ball.g, 1) == 1 and round(self.ball.b, 1) == 1:
            self.update_color()

    def update(self, dt):
        self.ball.move()

        self.update_size()

        self.update_color()

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


class PongBall(Widget):
    ball = ObjectProperty(None)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    r = NumericProperty(1)
    g = NumericProperty(1)
    b = NumericProperty(1)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.05
            ball.velocity = vel.x, vel.y + offset


if __name__ == '__main__':
    PongApp().run()

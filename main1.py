from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.image import Image
from random import randint
from kivy.uix.floatlayout import FloatLayout


class Dinosaur(Image):
    is_jumping = BooleanProperty(False)
    jump_height = NumericProperty(200)
    jump_speed = NumericProperty(300)
    gravity = NumericProperty(600)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'images/t-rex.png'
        self.size_hint = (None, None)
        self.size = (100, 100)
        self.pos_hint = {'center_x': 0.1, 'center_y': 0.3}
        self.velocity_y = 0

    def update(self, dt):
        if self.is_jumping:
            self.velocity_y += self.jump_speed * dt
            self.y += self.velocity_y * dt
            if self.y >= self.jump_height:
                self.velocity_y = 0
                self.is_jumping = False
        else:
            self.velocity_y -= self.gravity * dt
            self.y += self.velocity_y * dt

        if self.y <= 0:
            self.velocity_y = 0
            self.y = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = self.jump_speed

class Obstacle(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'images/cactus-big.png'
        self.size_hint = (None, None)
        self.size = (100, 100)
        self.pos_hint = {'center_x': 1, 'center_y': 0.3}
        self.velocity_x = 300

    def update(self, dt):
        self.x -= self.velocity_x * dt
        if self.x < -self.width:
            self.reset_position()

    def reset_position(self):
        self.x = Window.width + randint(100, 500)
        self.y = 0


class Background(FloatLayout):
    cloud_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create textures
        with self.canvas.before:
            self.cloud_texture = Image(source='bg.jpg').texture
            self.cloud_texture.wrap = 'repeat'
            self.cloud_texture.uvsize = (self.width / self.cloud_texture.width, -1)

    def on_size(self, *args):
        # Update uvsize when size changes
        self.cloud_texture.uvsize = (self.width / self.cloud_texture.width, -1)

class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background = Background()
        self.dinosaur = Dinosaur()
        self.obstacle = Obstacle()
        self.point = Point()  # Create an instance of Point
        self.add_widget(self.background)
        self.add_widget(self.dinosaur)
        self.add_widget(self.obstacle)
        self.add_widget(self.point)  # Add Point widget to the game
        Clock.schedule_interval(self.update, 1 / 60)

    def update(self, dt):
        self.dinosaur.update(dt)
        self.obstacle.update(dt)
        if self.dinosaur.collide_widget(self.obstacle):
            self.game_over()

    def game_over(self):
        self.remove_widget(self.dinosaur)
        self.remove_widget(self.obstacle)
        self.add_widget(
            Label(text='Game Over', font_size=50, pos_hint={'center_x': 0.5, 'center_y': 0.5}))

    def on_touch_down(self, touch):
        self.dinosaur.jump()

class Point(Label):
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = (1, 1, 1, 1)  # White color
        self.font_size = '24sp'
        self.pos_hint = {'right': 1, 'top': 1}  # Position at top right corner
        self.text = str(self.score)  # Display initial score
        Clock.schedule_interval(self.update_score, 0.07)  # Update score 

    def update_score(self, dt):
        self.score += 1
        self.text = str(self.score)  # Update displayed score

class T_RexApp(App):
    def build(self):
        return Game()

if __name__ == '__main__':
    T_RexApp().run()

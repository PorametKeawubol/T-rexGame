from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Ellipse, Rectangle
from kivy.uix.label import Label
from random import randint

class Background(Widget):
    cloud_texture = ObjectProperty(None)
    score_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set up cloud texture
        self.cloud_texture = 'images/cloud-small.png'

        # Set up background image
        with self.canvas.before:
            # Draw a rectangle for the background image
            self.bg = Rectangle(source='sky.png', size=Window.size, pos=self.pos)

            # Draw clouds using Ellipse
            self.cloud_1 = Ellipse(pos=(0, Window.height * 0.75), size=(200, 100))
            self.cloud_2 = Ellipse(pos=(Window.width * 0.5, Window.height * 0.6), size=(150, 80))

        # Create label for displaying score
        self.score_label = Label(text='0', color=(0, 0, 0, 1), font_size='24sp', size_hint=(None, None), size=(100, 50),
                                  pos_hint={'right': 1, 'top': 1})

        self.add_widget(self.score_label)  # Add the label to the background widget

    def scroll_textures(self, time_passed):
        # Set up cloud movement
        self.cloud_1.pos = (self.cloud_1.pos[0] + time_passed * 50, self.cloud_1.pos[1])
        self.cloud_2.pos = (self.cloud_2.pos[0] + time_passed * 50, self.cloud_2.pos[1])
        if self.cloud_1.pos[0] > Window.width:
            self.cloud_1.pos = (-200, Window.height * 0.75)
        if self.cloud_2.pos[0] > Window.width:
            self.cloud_2.pos = (-150, Window.height * 0.6)

class Dinosaur(Image):
    is_jumping = False
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

class Obstacle(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (100, 100)
        self.pos_hint = {'center_x': 1, 'center_y': 0.3}
        self.velocity_x = 300

        # Set up cactus image
        with self.canvas:
            self.floor_texture = Rectangle(source='images/floor.png', size=self.size, pos=self.pos)
            self.cactus_texture = Rectangle(source='images/cactus-big.png', size=self.size, pos=(self.x, self.y))

    def update(self, dt):
        self.x -= self.velocity_x * dt
        self.cactus_texture.pos = (self.x, self.y + 50)  # Update cactus position along with the obstacle
        self.floor_texture.pos = self.pos  # Update floor position along with the obstacle
        if self.x < -self.width:
            self.reset_position()

    def reset_position(self):
        self.x = Window.width + randint(100, 500)
        self.y = 0
        self.cactus_texture.pos = (self.x, self.y + 100)  # Reset cactus position along with the obstacle
        self.floor_texture.pos = self.pos  # Reset floor position along with the obstacle

class Point(Widget):
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_score, 0.07)  # Update score

    def update_score(self, dt):
        self.parent.background.score_label.text = str(self.score)  # Update displayed score

class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background = Background()
        self.dinosaur = Dinosaur()
        self.obstacle = Obstacle()
        self.point = Point()  # Create an instance of Point
        self.game_over_label = Label(text='Game Over', font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.background)
        self.add_widget(self.dinosaur)
        self.add_widget(self.obstacle)
        self.add_widget(self.point)  # Add Point widget to the game
        Clock.schedule_interval(self.update, 1 / 60)
        Clock.schedule_interval(self.background.scroll_textures, 0.1)  # Scroll textures every 0.1 seconds

    def update(self, dt):
        self.dinosaur.update(dt)
        self.obstacle.update(dt)
        if self.dinosaur.collide_widget(self.obstacle):
            self.game_over()

    def game_over(self):
        self.remove_widget(self.dinosaur)
        self.remove_widget(self.obstacle)
        self.add_widget(self.game_over_label)

    def on_touch_down(self, touch):
        self.dinosaur.jump()

class T_RexApp(App):
    def build(self):
        return Game()

if __name__ == '__main__':
    T_RexApp().run()

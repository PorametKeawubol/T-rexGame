from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Ellipse, Rectangle
from kivy.uix.label import Label
from random import randint
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from StartPage import StartPage
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.image import Image as CoreImage
from AnimatedDinosaur import AnimatedDinosaur



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

            # Draw clouds using Rectangles 
            self.cloud_1 = Rectangle(texture=Image(source='images/cloud-big.png').texture, pos=(Window.width, Window.height * 0.75), size=(220, 140))
            self.cloud_2 = Rectangle(texture=Image(source='images/cloud-small.png').texture, pos=(Window.width * 0.5, Window.height * 0.6), size=(160, 90))

        # Create label for displaying score
        self.score_label = Label(text='0', color=(0, 0, 0, 1), font_size='24sp', size_hint=(None, None), size=(100, 50),
                                  pos=(Window.width - 100, Window.height - 50))
        self.bind(pos=self.update_score_label_position)

        self.add_widget(self.score_label)  # Add the label to the background widget

        # Bind the size of the background image to the size of the window
        Window.bind(size=self.on_window_size_changed)

    def update_score_label_position(self, *args):
        # Update the position of the score label
        self.score_label.pos = (Window.width - self.score_label.width - 10, Window.height - self.score_label.height - 10)

    def scroll_textures(self, time_passed):
        # Set up cloud movement
        if hasattr(self, 'cloud_1') and hasattr(self, 'cloud_2'):  # Check if clouds exist
            self.cloud_1.pos = (self.cloud_1.pos[0] - time_passed * 50, self.cloud_1.pos[1])
            self.cloud_2.pos = (self.cloud_2.pos[0] - time_passed * 80, self.cloud_2.pos[1])
            if self.cloud_1.pos[0] + self.cloud_1.size[0] < 0:
                self.cloud_1.pos = (Window.width, Window.height * 0.75)
            if self.cloud_2.pos[0] + self.cloud_2.size[0] < 0:
                self.cloud_2.pos = (Window.width, Window.height * 0.6)

    def on_window_size_changed(self, instance, size):
        # Update the size of the background image when the window size changes
        self.bg.size = size
        self.update_score_label_position()  # Call the method to update the score label position



class Dinosaur(Image):
    is_jumping = False
    jump_height = NumericProperty(250)
    jump_speed = NumericProperty(300)
    gravity = NumericProperty(600)
    jump_sound = SoundLoader.load('sounds/dino_jump.wav')  # Load the jump sound effect


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'images/t-rex.png'
        self.size_hint = (None, None)
        self.size = (100, 100)
        self.pos_hint = {'center_x': 0.1, 'center_y': 0.3}
        self.velocity_y = 0
        self.center_x = Window.width / 3 

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

        if self.y <= self.parent.floor.floor_height -38:  
            self.velocity_y = 0
            self.y = self.parent.floor.floor_height -38
            self.is_jumping = False

        if self.y <= 0:
            self.velocity_y = 0
            self.y = 0
            self.is_jumping = False
    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = self.jump_speed
            if self.jump_sound:
                self.jump_sound.volume = 1  # Adjust the volume of the jump sound effect
                self.jump_sound.play()  # Play the jump sound effect

class Floor(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.floor_height = 100  # Define the height of the floor
        self.velocity_x = 300

        # Load the floor texture
        floor_texture_source = 'images/floor.png'
        floor_texture_size = (200, self.floor_height)  # Define the size of each floor texture

        # Create a list to hold floor textures
        self.floor_textures = []

        # Calculate the number of floor textures needed to cover the screen width
        num_textures = (Window.width // floor_texture_size[0]) + 8  # Add 2 textures for scrolling effect

        # Create and position floor textures
        for i in range(num_textures):
            floor_texture = Rectangle(source=floor_texture_source, size=floor_texture_size,
                                      pos=(i * floor_texture_size[0], 0))
            self.floor_textures.append(floor_texture)
            self.canvas.add(floor_texture)

    def update(self, dt):
        # Move floor textures horizontally
        for texture in self.floor_textures:
            texture.pos = (texture.pos[0] - self.velocity_x * dt, texture.pos[1])

            # Check if the texture has moved off-screen to the left
            if texture.pos[0] + texture.size[0] < 0:
                # Move the texture to the right of the screen
                texture.pos = (texture.pos[0] + len(self.floor_textures) * texture.size[0], texture.pos[1])

class Obstacle(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (100, 100)
        self.pos_hint = {'center_x': 1, 'center_y': 0.3}
        self.velocity_x = 300

        # Set up cactus image
        with self.canvas:
            self.cactus_texture = Rectangle(source='images/cactus-big.png', size=self.size, pos=(self.x, self.y))

    def update(self, dt):
        self.x -= self.velocity_x * dt
        self.cactus_texture.pos = (self.x, self.y + 50)  # Update cactus position
        if self.x < -self.width:
            self.reset_position()

    def reset_position(self):
        self.x = Window.width + randint(100, 500)
        self.y = 0
        self.cactus_texture.pos = (self.x, self.y + 100)  # Reset cactus position

class Point(Widget):
    score = NumericProperty(0)
    game_over = False  # Add a flag to track game over state
    checkpoint_sound = SoundLoader.load('sounds/dino_checkpoint.wav')  # Load the checkpoint sound effect

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score_increment = Clock.schedule_interval(self.update_score, 0.07)  # Schedule score update

    def update_score(self, dt):
        if not self.game_over:  # Check if the game is not over
            self.score += 1  # Increment the score by 1
            self.parent.background.score_label.text = str(self.score)  # Update displayed score

        # Check if the score is a multiple of 100 and has '00' at the end
            if self.score % 100 == 0 and self.score % 1000 != 0:
                if self.checkpoint_sound:
                    self.checkpoint_sound.play()  # Play the checkpoint sound effect

            # Increase game speed slightly when score reaches multiples of 100
                self.parent.floor.velocity_x += 50 # Increase floor velocity
                self.parent.dinosaur.jump_speed += 50
                self.parent.obstacle.velocity_x += 50
    def stop_score_increment(self):
        Clock.unschedule(self.update_score)  # Stop incrementing score

    def start_score_increment(self):
        self.score_increment = Clock.schedule_interval(self.update_score, 0.07)  # Resume score incrementing
        
class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize game state
        self.game_over = False
        self.paused = False
        self.game_clock = None
        self.background = None
        self.dinosaur = None
        self.obstacle = None
        self.floor = None
        self.point = None
        self.background_music = None
        self.pause_image = None
        self.game_over_image = None
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self.initialize_game()
        

    def initialize_game(self):
        # Reset game state
        self.clear_widgets()
        self.background = Background()
        self.dinosaur = Dinosaur()
        self.obstacle = Obstacle()
        self.floor = Floor()
        self.point = Point()
        self.add_widget(self.background)
        self.add_widget(self.dinosaur)
        self.add_widget(self.obstacle)
        self.add_widget(self.floor)
        self.add_widget(self.point)
        self.point.game_over = False
        self.background_music = SoundLoader.load('sounds/cottagecore-17463.mp3')
        if self.background_music:
            self.background_music.loop = True
            self.background_music.play()
        self.paused = False
        self.game_over = False
        self.game_clock = None
        Clock.schedule_interval(self.update, 1 / 60)
        Clock.schedule_interval(self.background.scroll_textures, 1/60)
        self.pause_image = Image(source="images/PAUSE.png", size_hint=(None, None), size=(100, 50),
                                 pos=(10, Window.height - 60))
        self.pause_image.bind(on_press=self.toggle_pause)
        self.add_widget(self.pause_image)

    def toggle_pause(self, instance):
        if self.paused:
            Clock.schedule_interval(self.update, 1 / 60)
            Clock.schedule_interval(self.background.scroll_textures, 1/60)
            self.paused = False
            self.pause_image.source = "images/PAUSE.png"
            self.point.start_score_increment()
        else:
            Clock.unschedule(self.update)
            Clock.unschedule(self.background.scroll_textures)
            self.paused = True
            self.pause_image.source = "images/RESUME.png"
            self.point.stop_score_increment()

    def update(self, dt):
        if not self.game_over:
            self.dinosaur.update(dt)
            self.obstacle.update(dt)
            self.floor.update(dt)
            if self.dinosaur.collide_widget(self.obstacle):
                self.game_over = True
                self.game_over_actions()

    def game_over_actions(self):
        if not self.game_clock:
            try:
                Clock.unschedule(self.update)
                Clock.unschedule(self.background.scroll_textures)
            except:
                pass
            self.game_over_image = Image(source='images/GAME-OVER.png', size_hint=(None, None), size=(400, 200),
                             pos=(Window.width / 2 - 200, Window.height / 2 + 25))
            self.add_widget(self.game_over_image)
            self.background_music.stop()
            game_over_music = SoundLoader.load('sounds/NeverGiveUp.mp3')
            if game_over_music:
                game_over_music.volume = 0.2
                game_over_music.play()
            self.point.game_over = True
            self.point.stop_score_increment()
            
    def on_touch_down(self, touch):
        if not self.game_over:  # ตรวจสอบว่าเกมยังไม่จบ
            if self.pause_image.collide_point(*touch.pos):  # ตรวจสอบว่าที่คลิกอยู่บนปุ่ม pause/resume
                self.toggle_pause(self.pause_image)  # เรียกเมธอด toggle_pause เพื่อ pause หรือ resume เกม
            else:  # ถ้าไม่ได้คลิกที่ปุ่ม pause/resume
                self.dinosaur_jump(touch)  # เรียกเมธอดให้ดิโนเสาร์กระโดด
    
    def dinosaur_jump(self, touch=None):
        if self.dinosaur.y == self.floor.floor_height - 38:  # Check if the dinosaur is on the ground
          self.dinosaur.jump()

    def stop_game(self):
        # Stop the game completely
        if not self.game_clock:
            try:
                Clock.unschedule(self.update)  # Stop the game update loop
                Clock.unschedule(self.background.scroll_textures)  # Stop scrolling textures
            except:
                pass  # Handle case when clock is already unscheduled
            self.game_over = True

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Handle keyboard events
        if not self.game_over:
            if keycode[1] == 'spacebar':  # Check if the key pressed is the spacebar
                self.dinosaur_jump()

class T_RexApp(App):
    def build(self):
        return StartPage()

if __name__ == '__main__':
    T_RexApp().run()

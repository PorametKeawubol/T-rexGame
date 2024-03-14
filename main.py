
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
            self.cloud_1 = Ellipse(texture=Image(source='images/cloud-big.png').texture, pos=(Window.width, Window.height * 0.75), size=(200, 100))
            self.cloud_2 = Ellipse(texture=Image(source='images/cloud-small.png').texture, pos=(Window.width * 0.5, Window.height * 0.6), size=(150, 80))

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
        self.source = 'images/image01.jpg'
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
        num_textures = (Window.width // floor_texture_size[0]) + 2  # Add 2 textures for scrolling effect

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

    def stop_score_increment(self):
        Clock.unschedule(self.update_score)  # Stop incrementing score

    def start_score_increment(self):
        self.score_increment = Clock.schedule_interval(self.update_score, 0.07)  # Resume score incrementing
        
class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background = Background()
        self.dinosaur = Dinosaur()
        self.obstacle = Obstacle()
        self.floor = Floor()  # Create an instance of Floor
        self.point = Point()  # Create an instance of Point
        self.add_widget(self.background)
        self.add_widget(self.dinosaur)
        self.add_widget(self.obstacle)
        self.add_widget(self.floor)  # Add floor to the game
        self.add_widget(self.point) 
        self.point.game_over = False  # Initialize the game_over flag
        self.background_music = SoundLoader.load('sounds/cottagecore-17463.mp3')  # Load background music
        if self.background_music:
            self.background_music.loop = True
            self.background_music.play()  # Start playing background music
        self.game_over = False  # Initialize game over state
        self.game_clock = None  # Initialize game clock reference
        Clock.schedule_interval(self.update, 1 / 60)
        Clock.schedule_interval(self.background.scroll_textures, 1/60)
          # Scroll textures every 0.1 seconds

        # Create pause button
        self.pause_button = Button(text="Pause", size_hint=(None, None), size=(100, 50),
                                   pos=(10, Window.height - 60))
        self.pause_button.bind(on_press=self.toggle_pause)
        self.add_widget(self.pause_button)

    def toggle_pause(self, instance):
        if self.game_clock:  # If the game is running
            Clock.unschedule(self.update)  # Stop the game update loop
            Clock.unschedule(self.background.scroll_textures)  # Stop scrolling textures
            self.game_clock = None  # Set game clock to None
            self.pause_button.text = "Resume"
        else:  # If the game is paused
            self.game_clock = Clock.schedule_interval(self.update, 1 / 60)  # Resume game update loop
            Clock.schedule_interval(self.background.scroll_textures, 1/60)  # Resume scrolling textures
            self.pause_button.text = "Pause"

    def update(self, dt):
        if not self.game_over:  # Check if the game is not over
            self.dinosaur.update(dt)
            self.obstacle.update(dt)
            self.floor.update(dt)  # Update floor position
            if self.dinosaur.collide_widget(self.obstacle):
                self.game_over = True
                self.game_over_actions()

    def game_over_actions(self):
        if not self.game_clock:
            try:
                Clock.unschedule(self.update)  # Stop the game update loop
                Clock.unschedule(self.background.scroll_textures)  # Stop scrolling textures
            except:
                pass  # Handle case when clock is already unscheduled
            self.add_widget(
    Label(text='Game Over', font_size=50, pos=(Window.width/2, Window.height/2))
)

            self.background_music.stop()  # Stop playing the current background music
            # Load and play another song for game over
            
            game_over_music = SoundLoader.load('sounds/NeverGiveUp.mp3')
            if game_over_music:
                game_over_music.volume = 0.2  # Set the volume to 20%
                game_over_music.play()
            self.point.game_over = True  # Set game_over flag to True
            self.point.stop_score_increment()  # Stop score incrementation

    def on_touch_down(self, touch):
        if not self.game_over:  # Check if the game is not over
            self.dinosaur.jump()
        if self.pause_button.collide_point(*touch.pos):  # Check if the touch is on the pause button
            self.toggle_pause(self.pause_button)

    def stop_game(self):
        # Stop the game completely
        if not self.game_clock:
            try:
                Clock.unschedule(self.update)  # Stop the game update loop
                Clock.unschedule(self.background.scroll_textures)  # Stop scrolling textures
            except:
                pass  # Handle case when clock is already unscheduled
            self.game_over = True

class T_RexApp(App):
    def build(self):
        return Game()

if __name__ == '__main__':
    T_RexApp().run()

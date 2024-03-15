from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.image import Image
import sys

class StartPage(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Set up the background
        self.background = Image(source='images/background.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)
        
        # Create a layout to center the button
        layout = AnchorLayout()
        layout.size_hint = (None, None)
        layout.size = (Window.width, Window.height)

        # Create a layout for the play button
        play_layout = AnchorLayout(anchor_x='center', anchor_y='top')
        play_layout.size_hint = (None, None)
        play_layout.size = (Window.width, Window.height / 2)

        # Create the play button
        play_button = Button(background_normal='images/PLAY.png', size_hint=(None, None), size=(200, 100))
        play_button.bind(on_press=self.on_play_button_press)
        play_layout.add_widget(play_button)

        # Add play_layout to the main layout
        layout.add_widget(play_layout)

        # Create a layout for the exit button
        exit_layout = AnchorLayout(anchor_x='center', anchor_y='bottom')
        exit_layout.size_hint = (None, None)
        exit_layout.size = (Window.width, Window.height / 2)

        # Create the exit button
        exit_button = Button(background_normal='images/EXIT.png', size_hint=(None, None), size=(200, 100))
        exit_button.bind(on_press=self.on_exit_button_press)
        exit_layout.add_widget(exit_button)

        # Add exit_layout to the main layout
        layout.add_widget(exit_layout)
        
        self.add_widget(layout)

    def on_play_button_press(self, instance):
        # Import Game class here to avoid circular import
        from main import Game

        # Switch to the game page when the button is pressed
        game_page = Game()
        self.parent.add_widget(game_page)
        self.parent.remove_widget(self)

    def on_exit_button_press(self, instance):
        # Exit the program when the button is pressed
        sys.exit()

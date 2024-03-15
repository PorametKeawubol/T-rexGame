from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.image import Image

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

        # Create the play button
        play_button = Button(background_normal='images/PLAY.png', size_hint=(None, None), size=(200, 100))
        play_button.bind(on_press=self.on_play_button_press)
        layout.add_widget(play_button)
        
        self.add_widget(layout)

    def on_play_button_press(self, instance):
        # Import Game class here to avoid circular import
        from main import Game

        # Switch to the game page when the button is pressed
        game_page = Game()
        self.parent.add_widget(game_page)
        self.parent.remove_widget(self)

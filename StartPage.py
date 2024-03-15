from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button


class StartPage(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.padding = 20
        self.spacing = 20
        self.background_color = (0.5, 0.5, 0.5, 1)  # Gray background color

        play_button = Button()
        play_button.size_hint = (None, None)
        play_button.size = (200, 100)
        play_button.background_normal = 'images/PLAY.png'
        play_button.background_down = 'images/PLAY.png'
        play_button.bind(on_press=self.on_play_button_press)

        self.add_widget(play_button)

    def on_play_button_press(self, instance):
        print("Play button pressed!")


class MyApp(App):
    def build(self):
        return StartPage()


if __name__ == '__main__':
    MyApp().run()
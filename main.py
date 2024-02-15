from kivy.app import App
from  kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window

class Background(Widget):
    cloud_texture = ObjectProperty(None)
    
    def  __init__(self, **kwargs):
        super().__init__(**kwargs)

        #Create textures
        self.cloud_texture = Image(source= 'images/cloud-small.png').texture
        self.cloud_texture.wrap = 'repeat'
        self.cloud_texture.uvsize = (Window.width / self.cloud_texture.width, -1)
    
    def scroll_textures(self, time_passed):
        self.cloud_texture.uvpos = ( (self.cloud_texture.uvpos[0] + time_passed/2.0)%Window.width, self.cloud_texture.uvpos[1])
        #
        texture = self.property('cloud_texture')
        texture.dispatch(self)
       
    pass

from kivy.clock import Clock
class MainApp(App):
    def on_start(self):
        Clock.schedule_interval(self.root.ids.background.scroll_textures, 1/60)
    pass

MainApp().run()
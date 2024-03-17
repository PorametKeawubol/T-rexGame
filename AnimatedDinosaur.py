from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.base import runTouchApp

class AnimatedDinosaur(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frames = []  # List to store the frames of the animation
        self.current_frame = 0  # Index of the current frame
        self.frame_duration = 0.1  # Duration (in seconds) for each frame
        self.is_animating = False  # Flag to indicate whether the animation is playing
        self.load_frames()  # Load frames of the animation
        self.frame_update = Clock.schedule_interval(self.update_frame, self.frame_duration)

    def load_frames(self):
        # Load individual frames of the animation
        for i in range(1, 11):  # Assuming there are 10 frames numbered from 1 to 10
            frame_source = f'images/sheets/DinoSprites - vita{i}.png'  # Adjust path and naming convention as needed
            frame = Image(source=frame_source)
            self.frames.append(frame)

    def update_frame(self, dt):
        if self.is_animating:
            # Display the current frame
            self.texture = self.frames[self.current_frame].texture

            # Move to the next frame
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def start_animation(self):
        # Start playing the animation
        self.is_animating = True

    def stop_animation(self):
        # Stop playing the animation
        self.is_animating = False

if __name__ == '__main__':
    # Create an instance of the AnimatedDinosaur widget
    animated_dinosaur = AnimatedDinosaur()

    # Run the app by passing the widget instance after a slight delay
    Clock.schedule_once(lambda dt: runTouchApp(animated_dinosaur), 0.1)
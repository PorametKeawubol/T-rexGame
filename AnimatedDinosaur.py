from kivy.uix.image import Image
from kivy.clock import Clock

class AnimatedDinosaur(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'images/sheets/DinoSprites - vita.png'  # Set the source image
        self.frame_width = 100  # Width of each frame in the sprite sheet
        self.frame_height = 100  # Height of each frame in the sprite sheet
        self.num_frames = 10  # Total number of frames in the sprite sheet
        self.current_frame = 0  # Index of the current frame
        self.frame_duration = 0.1  # Duration (in seconds) for each frame

        # Schedule the update of frames
        self.frame_update = Clock.schedule_interval(self.update_frame, self.frame_duration)

    def update_frame(self, dt):
        # Calculate the position of the current frame in the sprite sheet
        frame_x = self.current_frame * self.frame_width
        frame_y = 0  # Assuming all frames are in the same row

        # Set the texture coordinates to display the current frame
        self.texture = self.texture.get_region(frame_x, frame_y, self.frame_width, self.frame_height)

        # Increment or decrement the current frame based on direction
        self.current_frame += 1

        # If reached the end or beginning, reverse direction
        if self.current_frame >= self.num_frames or self.current_frame <= 0:
            self.frame_duration *= -1  # Reverse the frame update direction

        # Clamp the current frame index within range
        self.current_frame = min(max(0, self.current_frame), self.num_frames - 1)

    def stop_animation(self):
        # Stop the frame update schedule
        if self.frame_update:
            self.frame_update.cancel()

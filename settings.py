# This file will be used to manage the game's settings.

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initilize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (135, 206, 235)

        # Ship settings
        self.ship_speed = 3.0 # Speed of the ship moves 3.0 pixels per frame.
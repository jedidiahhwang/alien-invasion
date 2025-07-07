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

        # Bullet settings
        self.bullet_speed = 5.0 # Speed of the bullet moves 1.0 pixels per frame.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3 # Number of bullets allowed on the screen at a time.
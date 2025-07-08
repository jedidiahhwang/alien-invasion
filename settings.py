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
        self.ship_limit = 3 # Number of ships the player starts with.

        # Bullet settings
        self.bullet_speed = 7.0 # Speed of the bullet moves 7.0 pixels per frame.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3 # Number of bullets allowed on the screen at a time.

        # Alien settings
        self.alien_speed = 1.0 # Speed of the alien moves 1.0 pixels per frame.
        self.fleet_drop_speed = 50 # How quickly the fleet drops down the screen.
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
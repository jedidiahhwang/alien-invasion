import pygame

class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        
        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        
        # Set the background color of the image to be transparent
        # If it's a different color, change this value to match
        self.image.set_colorkey((230, 230, 230))  # Makes white background transparent
        
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        # This is because the rect.x is an integer, and we need to be able to move the ship by a decimal value.
        # rect only accepts integers.
        self.x = float(self.rect.x)

        # Movement flag; start with a ship that's not moving.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right: # Check if the ship is not at the right edge of the screen.
            self.x += self.settings.ship_speed # Recall that self.x is a decimal value.
        elif self.moving_left and self.rect.left > 0: # Check if the ship is not at the left edge of the screen. 0 is the left edge of the screen.
            self.x -= self.settings.ship_speed

        # Update rect object from self.x.
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
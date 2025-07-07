import pygame

class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        
        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        
        # Set the background color of the image to be transparent
        # If it's a different color, change this value to match
        self.image.set_colorkey((230, 230, 230))  # Makes white background transparent
        
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Movement flag; start with a ship that's not moving.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right:
            self.rect.x += 1
        elif self.moving_left:
            self.rect.x -= 1

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
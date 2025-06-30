import sys
import time
import pygame

from settings import Settings

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        # Establish a clock tick to manage frame rates.
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Validate settings to prevent performance issues
        self._validate_settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Set the background color.
        self.bg_color = self.settings.bg_color

        # Performance monitoring variables
        self.fps_counter = 0
        self.fps_timer = time.time()
        self.running = True

        # Cache font for performance
        self.font = pygame.font.Font(None, 36)

    def _validate_settings(self):
        """Validate settings to ensure optimal performance."""
        # Ensure reasonable screen dimensions
        if self.settings.screen_width > 1920:
            self.settings.screen_width = 1920
        if self.settings.screen_height > 1080:
            self.settings.screen_height = 1080
        
        # Ensure minimum dimensions for usability
        if self.settings.screen_width < 800:
            self.settings.screen_width = 800
        if self.settings.screen_height < 600:
            self.settings.screen_height = 600

    def _check_events(self):
        """Handle keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def _update_screen(self):
        """Update and draw the screen."""
        # Clear screen with background color
        self.screen.fill(self.bg_color)
        
        # Display performance info (optional, can be toggled)
        self._display_fps()
        
        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _display_fps(self):
        """Display current FPS for performance monitoring."""
        current_time = time.time()
        self.fps_counter += 1
        
        if current_time - self.fps_timer >= 1.0:  # Update every second
            fps_text = self.font.render(f"FPS: {self.fps_counter}", True, (0, 0, 0))
            self.screen.blit(fps_text, (10, 10))
            self.fps_counter = 0
            self.fps_timer = current_time

    def run_game(self):
        """Start the main loop for the game."""
        while self.running:
            # Watch for keyboard and mouse events.
            self._check_events()
            
            # Update game state (placeholder for future game logic)
            self._update_game()
            
            # Redraw the screen during each pass through the loop.
            self._update_screen()
            
            # Control frame rate - CRITICAL: This must be inside the loop
            self.clock.tick(60)  # 60 FPS target

        # Cleanup resources before exit
        self._cleanup()

    def _update_game(self):
        """Update game logic. Placeholder for future development."""
        # This method will contain game logic updates like:
        # - Moving sprites
        # - Collision detection
        # - Game state management
        pass

    def _cleanup(self):
        """Clean up resources before exiting."""
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
# This file will be used to manage the game's settings.

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings with performance considerations."""
        # Screen settings - optimized for common resolutions
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        
        # Performance settings
        self.fps_target = 60  # Target frames per second
        self.vsync_enabled = True  # Enable vertical sync for smooth display
        
        # Display settings
        self.fullscreen = False
        self.show_fps = True  # Show FPS counter for performance monitoring
        
        # Memory management settings
        self.max_cached_surfaces = 100  # Limit cached surfaces to prevent memory issues
        self.enable_dirty_updates = True  # Use dirty rectangle updates for better performance
        
        # Audio settings (for future development)
        self.audio_enabled = True
        self.audio_buffer_size = 512  # Smaller buffer for lower latency
        
        # Game performance settings
        self.max_entities = 1000  # Maximum number of game entities
        self.collision_optimization = True  # Enable spatial partitioning for collisions
        
    def get_display_mode(self):
        """Get display mode based on settings."""
        if self.fullscreen:
            return (0, 0)  # Fullscreen mode
        else:
            return (self.screen_width, self.screen_height)
    
    def get_display_flags(self):
        """Get pygame display flags based on settings."""
        import pygame
        flags = 0
        
        if self.fullscreen:
            flags |= pygame.FULLSCREEN
        
        if self.vsync_enabled:
            flags |= pygame.DOUBLEBUF
            
        return flags
"""
Optimized Alien Invasion Game with Performance Monitoring
This version implements all the performance optimizations identified in the analysis.
"""

import sys
import time
import pygame
from settings import Settings

# Import performance profiler if available
try:
    from performance_profiler import PerformanceProfiler
    PROFILER_AVAILABLE = True
except ImportError:
    PROFILER_AVAILABLE = False
    print("Performance profiler not available. Install psutil for full profiling.")

class OptimizedAlienInvasion:
    """Optimized version of the Alien Invasion game with performance monitoring."""

    def __init__(self):
        """Initialize the game with performance optimizations."""
        pygame.init()
        
        # Initialize settings and profiler
        self.settings = Settings()
        self.profiler = PerformanceProfiler() if PROFILER_AVAILABLE else None
        
        # Validate and optimize settings
        self._validate_and_optimize_settings()
        
        # Initialize display with optimized settings
        self._initialize_display()
        
        # Initialize game state
        self.running = True
        self.clock = pygame.time.Clock()
        
        # Performance monitoring
        self.fps_counter = 0
        self.fps_timer = time.time()
        self.performance_warnings = []
        
        # Optimize pygame settings
        self._optimize_pygame_settings()
        
        # Cache frequently used objects
        self._initialize_cached_objects()
        
    def _validate_and_optimize_settings(self):
        """Validate and optimize game settings for best performance."""
        # Clamp screen dimensions to reasonable limits
        self.settings.screen_width = max(800, min(1920, self.settings.screen_width))
        self.settings.screen_height = max(600, min(1080, self.settings.screen_height))
        
        # Optimize FPS target based on display capabilities
        if hasattr(pygame.display, 'get_desktop_sizes'):
            # Use pygame 2.0+ feature if available
            desktop_sizes = pygame.display.get_desktop_sizes()
            if desktop_sizes:
                # Adjust target FPS based on screen size
                screen_area = self.settings.screen_width * self.settings.screen_height
                if screen_area > 1920 * 1080:
                    self.settings.fps_target = 30  # Lower FPS for high-res displays
        
    def _initialize_display(self):
        """Initialize the display with optimized settings."""
        # Set display mode with performance flags
        flags = self.settings.get_display_flags()
        screen_size = self.settings.get_display_mode()
        
        self.screen = pygame.display.set_mode(screen_size, flags)
        pygame.display.set_caption("Alien Invasion - Optimized")
        
        # Convert screen surface for faster blitting
        if not self.settings.fullscreen:
            self.screen = self.screen.convert()
            
    def _optimize_pygame_settings(self):
        """Apply pygame-specific optimizations."""
        # Set event queue size to prevent overflow
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
        
        # Initialize audio with optimized settings if enabled
        if self.settings.audio_enabled:
            try:
                pygame.mixer.pre_init(
                    frequency=22050,  # Lower frequency for better performance
                    size=-16,
                    channels=2,
                    buffer=self.settings.audio_buffer_size
                )
                pygame.mixer.init()
            except pygame.error:
                print("Audio initialization failed. Continuing without audio.")
                self.settings.audio_enabled = False
                
    def _initialize_cached_objects(self):
        """Initialize and cache frequently used objects."""
        # Cache fonts for different sizes
        self.fonts = {
            'small': pygame.font.Font(None, 24),
            'medium': pygame.font.Font(None, 36),
            'large': pygame.font.Font(None, 48)
        }
        
        # Pre-render common text
        self.cached_text = {}
        
        # Cache background surface
        self.background = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        self.background.fill(self.settings.bg_color)
        self.background = self.background.convert()
        
    def _get_cached_text(self, text: str, font_size: str = 'medium', color: tuple = (0, 0, 0)):
        """Get cached text surface or create and cache if not exists."""
        cache_key = f"{text}_{font_size}_{color}"
        
        if cache_key not in self.cached_text:
            font = self.fonts.get(font_size, self.fonts['medium'])
            text_surface = font.render(text, True, color)
            self.cached_text[cache_key] = text_surface.convert_alpha()
            
            # Limit cache size to prevent memory issues
            if len(self.cached_text) > self.settings.max_cached_surfaces:
                # Remove oldest entries
                keys_to_remove = list(self.cached_text.keys())[:10]
                for key in keys_to_remove:
                    del self.cached_text[key]
                    
        return self.cached_text[cache_key]
        
    def _check_events(self):
        """Efficiently handle events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
                
    def _handle_keydown(self, event):
        """Handle keyboard input efficiently."""
        if event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.key == pygame.K_F1:
            # Toggle FPS display
            self.settings.show_fps = not self.settings.show_fps
        elif event.key == pygame.K_F2:
            # Export performance report
            if self.profiler:
                self.profiler.export_performance_data()
        elif event.key == pygame.K_F3:
            # Toggle fullscreen
            self._toggle_fullscreen()
            
    def _toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode."""
        self.settings.fullscreen = not self.settings.fullscreen
        
        # Reinitialize display
        flags = self.settings.get_display_flags()
        screen_size = self.settings.get_display_mode()
        self.screen = pygame.display.set_mode(screen_size, flags)
        
        # Recreate cached background
        self.background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        self.background.fill(self.settings.bg_color)
        self.background = self.background.convert()
        
    def _update_performance_monitoring(self):
        """Update performance monitoring and display."""
        if not self.settings.show_fps:
            return
            
        current_time = time.time()
        self.fps_counter += 1
        
        # Update FPS display every second
        if current_time - self.fps_timer >= 1.0:
            fps_text = f"FPS: {self.fps_counter}"
            
            # Add additional performance info if profiler is available
            if self.profiler:
                summary = self.profiler.get_performance_summary()
                fps_text += f" | Mem: {summary['memory_mb']:.1f}MB | CPU: {summary['cpu_percent']:.1f}%"
                
                # Check for performance warnings
                warnings = self.profiler.check_performance_warnings()
                if warnings != self.performance_warnings:
                    self.performance_warnings = warnings
                    if warnings:
                        print("Performance Warnings:")
                        for warning in warnings:
                            print(f"  - {warning}")
            
            # Clear old cached FPS text
            old_fps_keys = [key for key in self.cached_text.keys() if key.startswith("FPS:")]
            for key in old_fps_keys:
                del self.cached_text[key]
            
            self.fps_counter = 0
            self.fps_timer = current_time
            
    def _update_screen(self):
        """Optimized screen update with dirty rectangle support."""
        # Use cached background for faster clearing
        self.screen.blit(self.background, (0, 0))
        
        # Display performance information
        if self.settings.show_fps:
            current_time = time.time()
            if current_time - self.fps_timer >= 1.0 or not hasattr(self, '_fps_surface'):
                fps_text = f"FPS: {self.fps_counter}"
                if self.profiler:
                    summary = self.profiler.get_performance_summary()
                    fps_text += f" | Mem: {summary['memory_mb']:.1f}MB"
                
                self._fps_surface = self._get_cached_text(fps_text, 'small', (0, 0, 0))
            
            self.screen.blit(self._fps_surface, (10, 10))
        
        # Update display efficiently
        if self.settings.enable_dirty_updates:
            # In a full game, you would track dirty rectangles here
            pygame.display.flip()
        else:
            pygame.display.flip()
            
    def _update_game_logic(self):
        """Update game logic. Placeholder for future development."""
        # This is where game-specific logic would go:
        # - Entity updates
        # - Collision detection
        # - Game state management
        # - Physics simulation
        pass
        
    def run_game(self):
        """Run the optimized game loop."""
        print("Starting Optimized Alien Invasion...")
        print("Controls:")
        print("  ESC - Exit game")
        print("  F1  - Toggle FPS display")
        print("  F2  - Export performance report")
        print("  F3  - Toggle fullscreen")
        
        while self.running:
            # Start performance profiling for this frame
            if self.profiler:
                self.profiler.start_frame()
                
            # Handle events
            self._check_events()
            
            # Update game logic
            self._update_game_logic()
            
            # Update performance monitoring
            self._update_performance_monitoring()
            
            # Render the screen
            self._update_screen()
            
            # End performance profiling for this frame
            if self.profiler:
                self.profiler.end_frame()
            
            # Control frame rate
            self.clock.tick(self.settings.fps_target)
        
        # Cleanup and export final performance report
        self._cleanup()
        
    def _cleanup(self):
        """Clean up resources and export performance data."""
        if self.profiler:
            print("\nExporting final performance report...")
            self.profiler.export_performance_data("final_performance_report.txt")
            
            # Print final summary
            summary = self.profiler.get_performance_summary()
            print(f"\nFinal Performance Summary:")
            print(f"  Average FPS: {summary['fps']:.1f}")
            print(f"  Average Frame Time: {summary['avg_frame_time_ms']:.2f}ms")
            print(f"  Peak Memory Usage: {summary['memory_mb']:.1f}MB")
            print(f"  Total Runtime: {summary['runtime_seconds']:.1f}s")
            print(f"  Total Frames: {summary['total_frames']}")
        
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    # Create and run the optimized game
    game = OptimizedAlienInvasion()
    game.run_game()
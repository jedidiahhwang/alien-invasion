"""
Performance Profiler for Alien Invasion Game
Provides real-time performance monitoring and analysis tools.
"""

import time
import psutil
import gc
from collections import deque
from typing import Dict, List

class PerformanceProfiler:
    """A comprehensive performance profiler for pygame applications."""
    
    def __init__(self, max_samples: int = 60):
        """Initialize the profiler with specified sample buffer size."""
        self.max_samples = max_samples
        self.frame_times = deque(maxlen=max_samples)
        self.memory_usage = deque(maxlen=max_samples)
        self.cpu_usage = deque(maxlen=max_samples)
        
        self.last_frame_time = time.time()
        self.start_time = time.time()
        self.frame_count = 0
        
        # Performance thresholds
        self.fps_warning_threshold = 30
        self.memory_warning_threshold = 100  # MB
        self.cpu_warning_threshold = 80  # Percentage
        
    def start_frame(self):
        """Call at the beginning of each frame."""
        current_time = time.time()
        if self.frame_count > 0:  # Skip first frame
            frame_time = current_time - self.last_frame_time
            self.frame_times.append(frame_time)
        
        self.last_frame_time = current_time
        self.frame_count += 1
        
    def end_frame(self):
        """Call at the end of each frame to collect system metrics."""
        # Collect memory usage
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        self.memory_usage.append(memory_mb)
        
        # Collect CPU usage (non-blocking)
        cpu_percent = psutil.cpu_percent(interval=None)
        self.cpu_usage.append(cpu_percent)
        
    def get_fps(self) -> float:
        """Get current FPS based on recent frame times."""
        if not self.frame_times:
            return 0.0
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        return 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
    
    def get_average_frame_time(self) -> float:
        """Get average frame time in milliseconds."""
        if not self.frame_times:
            return 0.0
        return (sum(self.frame_times) / len(self.frame_times)) * 1000
    
    def get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        return self.memory_usage[-1] if self.memory_usage else 0.0
    
    def get_cpu_usage(self) -> float:
        """Get current CPU usage percentage."""
        return self.cpu_usage[-1] if self.cpu_usage else 0.0
    
    def get_performance_summary(self) -> Dict[str, float]:
        """Get a comprehensive performance summary."""
        return {
            'fps': self.get_fps(),
            'avg_frame_time_ms': self.get_average_frame_time(),
            'memory_mb': self.get_memory_usage(),
            'cpu_percent': self.get_cpu_usage(),
            'total_frames': self.frame_count,
            'runtime_seconds': time.time() - self.start_time
        }
    
    def check_performance_warnings(self) -> List[str]:
        """Check for performance issues and return warnings."""
        warnings = []
        
        fps = self.get_fps()
        if fps < self.fps_warning_threshold:
            warnings.append(f"Low FPS detected: {fps:.1f} (target: 60+)")
        
        memory = self.get_memory_usage()
        if memory > self.memory_warning_threshold:
            warnings.append(f"High memory usage: {memory:.1f}MB")
        
        cpu = self.get_cpu_usage()
        if cpu > self.cpu_warning_threshold:
            warnings.append(f"High CPU usage: {cpu:.1f}%")
        
        return warnings
    
    def optimize_performance(self):
        """Suggest and apply automatic optimizations."""
        warnings = self.check_performance_warnings()
        optimizations = []
        
        if any("memory" in warning.lower() for warning in warnings):
            # Force garbage collection
            collected = gc.collect()
            optimizations.append(f"Garbage collection freed {collected} objects")
        
        if any("fps" in warning.lower() for warning in warnings):
            optimizations.append("Consider reducing screen resolution or visual effects")
        
        if any("cpu" in warning.lower() for warning in warnings):
            optimizations.append("Consider optimizing game logic or reducing entity count")
        
        return optimizations
    
    def export_performance_data(self, filename: str = "performance_log.txt"):
        """Export performance data to a file for analysis."""
        with open(filename, 'w') as f:
            f.write("Alien Invasion Performance Report\n")
            f.write("=" * 40 + "\n\n")
            
            summary = self.get_performance_summary()
            for key, value in summary.items():
                f.write(f"{key.replace('_', ' ').title()}: {value:.2f}\n")
            
            f.write("\nPerformance Warnings:\n")
            warnings = self.check_performance_warnings()
            if warnings:
                for warning in warnings:
                    f.write(f"- {warning}\n")
            else:
                f.write("No performance issues detected.\n")
            
            f.write("\nOptimization Suggestions:\n")
            optimizations = self.optimize_performance()
            if optimizations:
                for opt in optimizations:
                    f.write(f"- {opt}\n")
            else:
                f.write("No optimizations needed.\n")
        
        print(f"Performance report exported to {filename}")

# Example usage integration
if __name__ == "__main__":
    # This shows how to integrate the profiler with the game
    profiler = PerformanceProfiler()
    
    # Simulate game loop
    for frame in range(100):
        profiler.start_frame()
        
        # Simulate some work
        time.sleep(0.016)  # ~60 FPS
        
        profiler.end_frame()
    
    # Print results
    summary = profiler.get_performance_summary()
    print("Performance Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value:.2f}")
    
    # Export detailed report
    profiler.export_performance_data()
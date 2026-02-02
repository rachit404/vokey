"""
Cursor Tracking and Feedback Components
========================================
Provides cursor position tracking, visual highlights, and audio feedback.

This module contains:
- CursorTracker: Tracks and stores cursor position
- CursorHighlighter: Shows visual highlight around cursor
- AudioFeedback: Plays audio beep feedback
"""

import threading
import tkinter as tk
import winsound
from typing import Optional, Tuple
try:
    import win32api
except ImportError:
    print("Warning: pywin32 not installed. Install with: pip install pywin32")
    win32api = None


class CursorTracker:
    """
    Tracks cursor position using Windows API.
    Stores position when recording starts for later retrieval.
    """
    
    def __init__(self):
        """Initialize the cursor tracker."""
        self.stored_position: Optional[Tuple[int, int]] = None
    
    def get_cursor_position(self) -> Tuple[int, int]:
        """
        Get the current cursor position.
        
        Returns:
            Tuple of (x, y) screen coordinates
        """
        if win32api is None:
            raise RuntimeError("pywin32 is not installed")
        
        try:
            x, y = win32api.GetCursorPos()
            return (x, y)
        except Exception as e:
            print(f"Error getting cursor position: {e}")
            return (0, 0)
    
    def store_position(self):
        """Store the current cursor position."""
        self.stored_position = self.get_cursor_position()
    
    def get_stored_position(self) -> Optional[Tuple[int, int]]:
        """
        Get the stored cursor position.
        
        Returns:
            Tuple of (x, y) coordinates, or None if not stored
        """
        return self.stored_position


class CursorHighlighter:
    """
    Shows a visual highlight around the cursor position.
    Uses a transparent tkinter window overlay.
    """
    
    def __init__(self, radius: int = 30, color: str = "#00AAFF", thickness: int = 3):
        """
        Initialize the cursor highlighter.
        
        Args:
            radius: Radius of the highlight circle in pixels
            color: Color of the highlight (hex format)
            thickness: Thickness of the circle border
        """
        self.radius = radius
        self.color = color
        self.thickness = thickness
    
    def highlight(self, x: int, y: int, duration: int = 500):
        """
        Show a highlight at the specified position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            duration: Duration in milliseconds (default 500ms)
        """
        # Run in a separate thread to avoid blocking
        thread = threading.Thread(target=self._show_highlight, args=(x, y, duration))
        thread.daemon = True
        thread.start()
    
    def _show_highlight(self, x: int, y: int, duration: int):
        """Internal method to create and show the highlight window."""
        try:
            # Create a transparent overlay window
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            
            # Create a topmost window
            overlay = tk.Toplevel(root)
            overlay.overrideredirect(True)  # Remove window decorations
            overlay.attributes('-topmost', True)  # Always on top
            overlay.attributes('-alpha', 0.7)  # Semi-transparent
            
            # Set window size and position
            size = self.radius * 2 + self.thickness * 2 + 4
            overlay.geometry(f"{size}x{size}+{x - size // 2}+{y - size // 2}")
            
            # Create canvas for drawing
            canvas = tk.Canvas(
                overlay,
                width=size,
                height=size,
                bg='black',
                highlightthickness=0
            )
            canvas.pack()
            
            # Make the background transparent (chroma key)
            overlay.wm_attributes('-transparentcolor', 'black')
            
            # Draw the circle
            padding = self.thickness // 2 + 2
            canvas.create_oval(
                padding,
                padding,
                size - padding,
                size - padding,
                outline=self.color,
                width=self.thickness,
                fill=''
            )
            
            # Auto-destroy after duration
            overlay.after(duration, lambda: self._cleanup(root, overlay))
            
            # Start the event loop
            root.mainloop()
            
        except Exception as e:
            print(f"Error showing cursor highlight: {e}")
    
    def _cleanup(self, root, overlay):
        """Clean up the overlay window."""
        try:
            overlay.destroy()
            root.destroy()
        except:
            pass


class AudioFeedback:
    """
    Provides audio feedback using system beeps.
    Uses Windows winsound module (built-in).
    """
    
    def __init__(self):
        """Initialize the audio feedback."""
        pass
    
    def play_beep(self, frequency: int = 800, duration: int = 100):
        """
        Play a system beep.
        
        Args:
            frequency: Frequency in Hz (37 to 32767)
            duration: Duration in milliseconds
        """
        # Run in a separate thread to avoid blocking
        thread = threading.Thread(target=self._play_beep, args=(frequency, duration))
        thread.daemon = True
        thread.start()
    
    def _play_beep(self, frequency: int, duration: int):
        """Internal method to play the beep."""
        try:
            winsound.Beep(frequency, duration)
        except Exception as e:
            print(f"Error playing beep: {e}")

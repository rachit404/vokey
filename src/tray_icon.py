"""
System Tray Icon Integration
=============================
Provides system tray icon with menu for background process management.
"""

import sys
from pathlib import Path
import pystray
from PIL import Image


class TrayIcon:
    """
    Manages the system tray icon and menu.
    Provides easy access to status and exit functionality.
    """
    
    def __init__(self, voice_assistant):
        """
        Initialize the tray icon.
        
        Args:
            voice_assistant: VoiceAssistant instance to control
        """
        self.voice_assistant = voice_assistant
        self.icon = None
    
    def _create_menu(self):
        """Create the system tray menu."""
        return pystray.Menu(
            pystray.MenuItem(
                "🎙️ Voice Assistant - Running",
                lambda: None,
                enabled=False
            ),
            pystray.MenuItem(
                "Show Status",
                self._show_status
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Exit",
                self._exit_app
            )
        )
    
    def _show_status(self, icon, item):
        """Show status notification."""
        status_msg = "Voice Assistant is running in background.\n"
        status_msg += f"Hotkey: {self.voice_assistant.hotkey.upper()}\n"
        status_msg += f"Status: {'Recording' if self.voice_assistant.recorder.is_recording else 'Waiting'}"
        
        # Show notification
        icon.notify(
            status_msg,
            title="Voice Assistant Status"
        )
    
    def _exit_app(self, icon, item):
        """Exit the application gracefully."""
        print("\n🛑 Exiting via system tray...")
        
        # Stop the voice assistant
        self.voice_assistant.stop()
        
        # Stop the tray icon
        icon.stop()
        
        # Exit the program
        sys.exit(0)
    
    def run(self):
        """
        Start the system tray icon.
        This is a blocking call - it will run until the icon is stopped.
        """
        # Load the icon image from artifacts folder
        icon_path = Path(__file__).parent.parent / "artifacts" / "favicon_io" / "favicon.ico"
        if not icon_path.exists():
            print(f"Warning: Icon file not found at {icon_path}")
            # Create a simple fallback icon
            icon_image = Image.new('RGB', (64, 64), color='blue')
        else:
            icon_image = Image.open(icon_path)
        
        # Create the tray icon
        self.icon = pystray.Icon(
            name="VoiceAssistant",
            icon=icon_image,
            title="Voice Assistant",
            menu=self._create_menu()
        )
        
        # Run the icon (blocking)
        print("✅ System tray icon started.")
        self.icon.run()


if __name__ == "__main__":
    print("This module should be imported, not run directly.")

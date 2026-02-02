"""
Background Launcher for Voice Assistant
========================================
Runs the voice assistant in background mode with system tray icon.
No console window will appear when this script is executed.

Usage:
    Double-click this file, or run: pythonw start_background.pyw
"""

import sys
import threading
import logging
from datetime import datetime
from main import VoiceAssistant
from tray_icon import TrayIcon


def setup_logging():
    """Setup file-based logging for background mode."""
    log_filename = f"vokey_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler(sys.stdout)  # Keep for debugging
        ]
    )
    
    return log_filename


def main():
    """Main entry point for background mode."""
    try:
        # Setup logging
        log_file = setup_logging()
        logging.info("="*60)
        logging.info("Voice Assistant - Background Mode")
        logging.info("="*60)
        logging.info(f"Logging to: {log_file}")
        
        # Configuration
        HOTKEY = "alt+r"
        WHISPER_MODEL = "base"
        
        # Create the voice assistant
        logging.info("Initializing voice assistant...")
        assistant = VoiceAssistant(hotkey=HOTKEY, whisper_model=WHISPER_MODEL)
        
        # Start the assistant in a separate thread
        logging.info("Starting voice assistant thread...")
        assistant_thread = threading.Thread(target=assistant.start, daemon=True)
        assistant_thread.start()
        
        # Create and run the system tray icon (blocking)
        logging.info("Starting system tray icon...")
        tray = TrayIcon(assistant)
        tray.run()  # This blocks until the user exits from the tray menu
        
    except KeyboardInterrupt:
        logging.info("\n\n🛑 Shutting down...")
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

"""
Windows Voice Assistant - CLI Version
======================================
Converts voice to text using OpenAI Whisper and types it at the cursor position.

Hotkey: Ctrl + M
- Press once: Start recording
- Press again: Stop recording, transcribe, and type text

Author: Voice Assistant
Version: 2.0.0
"""

import sys
import threading
import time
import keyboard
from core import AudioRecorder, WhisperTranscriber, TextTyper


class VoiceAssistant:
    """
    Main voice assistant orchestrator.
    Manages hotkey detection, recording, transcription, and typing.
    """
    
    def __init__(self, hotkey: str = "ctrl+shift+v", whisper_model: str = "base"):
        """
        Initialize the voice assistant.
        
        Args:
            hotkey: Keyboard hotkey to trigger recording (e.g., 'ctrl+shift+v')
            whisper_model: Whisper model name to use
        """
        self.hotkey = hotkey
        self.recorder = AudioRecorder()
        self.transcriber = WhisperTranscriber(model_name=whisper_model)
        self.typer = TextTyper()
        self.is_running = False
        self.processing_lock = threading.Lock()
    
    def _on_hotkey_toggle(self):
        """Called when hotkey is pressed - toggles recording on/off."""
        if self.recorder.is_recording:
            # Stop recording and process
            if not self.processing_lock.acquire(blocking=False):
                return
            
            try:
                # Stop recording and get audio
                audio_data = self.recorder.stop_recording()
                
                if len(audio_data) == 0:
                    print("⚠️  No audio recorded.")
                    return
                
                # Transcribe audio to text
                text = self.transcriber.transcribe(audio_data)
                
                if not text:
                    print("⚠️  No text transcribed.")
                    return
                
                # Type the text at the cursor position
                self.typer.type_text(text)
                
            finally:
                self.processing_lock.release()
        else:
            # Start recording
            if not self.processing_lock.locked():
                self.recorder.start_recording()
    
    def start(self):
        """Start the voice assistant (blocks until stopped)."""
        self.is_running = True
        
        print("\n" + "="*60)
        print("🎙️  VOICE ASSISTANT STARTED")
        print("="*60)
        print(f"Hotkey: {self.hotkey.upper()}")
        print("Press once to start recording.")
        print("Press again to stop recording and type text.")
        print("Press Ctrl+C to exit.")
        print("="*60 + "\n")
        
        # Register hotkey as a toggle
        keyboard.add_hotkey(self.hotkey, self._on_hotkey_toggle, suppress=False)
        
        try:
            # Keep the program running
            while self.is_running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down...")
            self.stop()
    
    def stop(self):
        """Stop the voice assistant."""
        self.is_running = False
        keyboard.unhook_all()
        print("✅ Voice assistant stopped.")


def main():
    """Main entry point."""
    # Configuration
    HOTKEY = "ctrl+m"  # Change this to customize the hotkey
    WHISPER_MODEL = "base"   # Options: tiny, base, small, medium, large
    
    # Create and start the assistant
    assistant = VoiceAssistant(hotkey=HOTKEY, whisper_model=WHISPER_MODEL)
    
    try:
        assistant.start()
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

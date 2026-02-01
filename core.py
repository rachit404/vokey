"""
Voice Assistant Core Components
=================================
Shared classes used by both CLI and GUI versions.

This module contains:
- AudioRecorder: Records audio from microphone
- WhisperTranscriber: Transcribes audio to text
- TextTyper: Types text at cursor position
"""

import sys
import queue
import time
import numpy as np
import sounddevice as sd
import whisper
import pyautogui
from typing import Optional


class AudioRecorder:
    """
    Records audio from the microphone using sounddevice.
    Stores audio chunks in a thread-safe queue.
    """
    
    def __init__(self, sample_rate: int = 16000):
        """
        Initialize the audio recorder.
        
        Args:
            sample_rate: Audio sample rate in Hz (Whisper expects 16kHz)
        """
        self.sample_rate = sample_rate
        self.audio_queue = queue.Queue()
        self.is_recording = False
        self.stream: Optional[sd.InputStream] = None
        
    def _audio_callback(self, indata, frames, time_info, status):
        """Callback function called by sounddevice for each audio block."""
        if status:
            print(f"Audio status: {status}", file=sys.stderr)
        if self.is_recording:
            self.audio_queue.put(indata.copy())
    
    def start_recording(self):
        """Start recording audio from the microphone."""
        if self.is_recording:
            return
        
        self.is_recording = True
        self.audio_queue = queue.Queue()  # Clear previous data
        
        try:
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,  # Mono audio
                callback=self._audio_callback,
                dtype=np.float32
            )
            self.stream.start()
            print("🎤 Recording started...")
        except Exception as e:
            print(f"Error starting recording: {e}", file=sys.stderr)
            self.is_recording = False
    
    def stop_recording(self) -> np.ndarray:
        """
        Stop recording and return the recorded audio.
        
        Returns:
            numpy array of audio data (float32, mono)
        """
        if not self.is_recording:
            return np.array([], dtype=np.float32)
        
        self.is_recording = False
        
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        
        print("🛑 Recording stopped.")
        
        # Collect all audio chunks
        audio_chunks = []
        while not self.audio_queue.empty():
            audio_chunks.append(self.audio_queue.get())
        
        if not audio_chunks:
            return np.array([], dtype=np.float32)
        
        # Concatenate all chunks into a single array
        audio_data = np.concatenate(audio_chunks, axis=0)
        return audio_data.flatten()


class WhisperTranscriber:
    """
    Transcribes audio to text using OpenAI Whisper (offline).
    Preloads the model for minimal latency.
    """
    
    def __init__(self, model_name: str = "base"):
        """
        Initialize the Whisper transcriber.
        
        Args:
            model_name: Whisper model size (tiny, base, small, medium, large)
                       'base' provides good balance of speed and accuracy
        """
        self.model_name = model_name
        print(f"📦 Loading Whisper model '{model_name}'... (this may take a moment)")
        try:
            self.model = whisper.load_model(model_name)
            print(f"✅ Whisper model '{model_name}' loaded successfully.")
        except Exception as e:
            print(f"Error loading Whisper model: {e}", file=sys.stderr)
            sys.exit(1)
    
    def transcribe(self, audio_data: np.ndarray) -> str:
        """
        Transcribe audio data to text.
        
        Args:
            audio_data: numpy array of audio samples (float32, 16kHz)
        
        Returns:
            Transcribed text string
        """
        if len(audio_data) == 0:
            return ""
        
        try:
            print("🔄 Transcribing...")
            # Whisper expects float32 audio normalized to [-1, 1]
            result = self.model.transcribe(audio_data, fp16=False)
            text = result["text"].strip()
            print(f"✅ Transcription: '{text}'")
            return text
        except Exception as e:
            print(f"Error during transcription: {e}", file=sys.stderr)
            return ""


class TextTyper:
    """
    Types text at the current cursor position using keyboard simulation.
    Does NOT use clipboard paste.
    """
    
    def __init__(self, typing_interval: float = 0.0):
        """
        Initialize the text typer.
        
        Args:
            typing_interval: Delay between characters (0 for instant typing)
        """
        self.typing_interval = typing_interval
        # Disable pyautogui fail-safe (moving mouse to corner won't stop it)
        pyautogui.FAILSAFE = False
    
    def type_text(self, text: str):
        """
        Type text at the current cursor position.
        
        Args:
            text: The text to type
        """
        if not text:
            return
        
        try:
            print(f"⌨️  Typing text...")
            # Small delay to ensure the application is ready to receive input
            time.sleep(0.1)
            pyautogui.write(text, interval=self.typing_interval)
            print("✅ Text typed successfully.")
        except Exception as e:
            print(f"Error typing text: {e}", file=sys.stderr)

"""
Voice Assistant GUI Application
================================
GUI version with text history storage and management.

Features:
- Modern tkinter interface
- SQLite database for history
- Delete individual or all items
- Copy to clipboard
- System tray integration
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import sqlite3
from datetime import datetime
from pathlib import Path
import keyboard
from core import AudioRecorder, WhisperTranscriber, TextTyper
from cursor_tracker import CursorTracker, CursorHighlighter, AudioFeedback


class DatabaseManager:
    """Manages SQLite database for transcription history."""
    
    def __init__(self, db_path: str = "history.db"):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create database and tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transcriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                text TEXT NOT NULL,
                duration REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_transcription(self, text: str, duration: float = None):
        """
        Add a new transcription to the database.
        
        Args:
            text: Transcribed text
            duration: Recording duration in seconds
        
        Returns:
            ID of the inserted record
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO transcriptions (timestamp, text, duration) VALUES (?, ?, ?)",
            (timestamp, text, duration)
        )
        
        row_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return row_id
    
    def get_all_transcriptions(self):
        """
        Get all transcriptions ordered by newest first.
        
        Returns:
            List of tuples (id, timestamp, text, duration)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, timestamp, text, duration FROM transcriptions ORDER BY id DESC"
        )
        results = cursor.fetchall()
        
        conn.close()
        return results
    
    def delete_transcription(self, transcription_id: int):
        """
        Delete a specific transcription.
        
        Args:
            transcription_id: ID of the transcription to delete
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM transcriptions WHERE id = ?", (transcription_id,))
        
        conn.commit()
        conn.close()
    
    def clear_all(self):
        """Delete all transcriptions."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM transcriptions")
        
        conn.commit()
        conn.close()
    
    def get_statistics(self):
        """
        Get statistics about transcriptions.
        
        Returns:
            Dictionary with count and total duration
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*), SUM(duration) FROM transcriptions")
        count, total_duration = cursor.fetchone()
        
        conn.close()
        
        return {
            "count": count or 0,
            "total_duration": total_duration or 0
        }


class VoiceAssistantGUI:
    """Main GUI application for voice assistant."""
    
    def __init__(self, root):
        """
        Initialize the GUI application.
        
        Args:
            root: tkinter root window
        """
        self.root = root
        self.root.title("🎙️ Voice Assistant")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Set window icon
        icon_path = Path(__file__).parent.parent / "artifacts" / "favicon_io" / "favicon.ico"
        if icon_path.exists():
            try:
                self.root.iconbitmap(icon_path)
            except Exception as e:
                print(f"Could not load icon: {e}")
        
        # Initialize components
        self.db = DatabaseManager()
        self.recorder = AudioRecorder()
        self.transcriber = WhisperTranscriber(model_name="base")
        self.typer = TextTyper()
        self.cursor_tracker = CursorTracker()
        self.cursor_highlighter = CursorHighlighter()
        self.audio_feedback = AudioFeedback()
        
        # State
        self.is_recording = False
        self.recording_start_time = None
        self.hotkey = "alt+r"
        
        # Build UI
        self.create_ui()
        
        # Load history
        self.refresh_history()
        
        # Register hotkey
        keyboard.add_hotkey(self.hotkey, self.toggle_recording, suppress=False)
        
        # Start status updater
        self.update_status()
    
    def create_ui(self):
        """Create all UI components."""
        # Status Frame
        status_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=10)
        status_frame.pack(fill=tk.X)
        
        self.status_label = tk.Label(
            status_frame,
            text="Status: Idle",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            fg="#2e7d32"
        )
        self.status_label.pack(side=tk.LEFT)
        
        hotkey_label = tk.Label(
            status_frame,
            text=f"Hotkey: {self.hotkey.upper()}",
            font=("Arial", 10),
            bg="#f0f0f0"
        )
        hotkey_label.pack(side=tk.RIGHT)
        
        # Control Frame
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.pack(fill=tk.X)
        
        self.record_btn = tk.Button(
            control_frame,
            text="🎤 Start Recording",
            command=self.toggle_recording,
            font=("Arial", 10, "bold"),
            bg="#4caf50",
            fg="white",
            padx=20,
            pady=10
        )
        self.record_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(
            control_frame,
            text="🗑️ Clear All",
            command=self.clear_all_history,
            font=("Arial", 10),
            bg="#f44336",
            fg="white",
            padx=20,
            pady=10
        )
        clear_btn.pack(side=tk.RIGHT, padx=5)
        
        # History Frame
        history_label_frame = tk.Frame(self.root, padx=10)
        history_label_frame.pack(fill=tk.X)
        
        self.history_count_label = tk.Label(
            history_label_frame,
            text="📝 Transcription History (0 items)",
            font=("Arial", 11, "bold")
        )
        self.history_count_label.pack(anchor=tk.W)
        
        # Scrollable history list
        history_container = tk.Frame(self.root, padx=10, pady=5)
        history_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas and scrollbar for custom scrolling
        canvas = tk.Canvas(history_container, bg="white")
        scrollbar = tk.Scrollbar(history_container, orient=tk.VERTICAL, command=canvas.yview)
        
        self.history_frame = tk.Frame(canvas, bg="white")
        
        self.history_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.history_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas = canvas
    
    def toggle_recording(self):
        """Toggle recording on/off."""
        if self.is_recording:
            # Stop recording
            self.is_recording = False
            self.status_label.config(text="Status: Processing...", fg="#ff9800")
            self.record_btn.config(text="🎤 Start Recording", bg="#4caf50")
            
            # Process in background thread
            threading.Thread(target=self.process_recording, daemon=True).start()
        else:
            # Start recording
            self.is_recording = True
            self.recording_start_time = time.time()
            
            # Store cursor position
            self.cursor_tracker.store_position()
            pos = self.cursor_tracker.get_stored_position()
            
            # Show visual feedback at cursor
            if pos:
                self.cursor_highlighter.highlight(pos[0], pos[1], duration=500)
            
            # Play audio feedback
            self.audio_feedback.play_beep(frequency=800, duration=100)
            
            # Start recording
            self.recorder.start_recording()
            self.status_label.config(text="Status: Recording...", fg="#f44336")
            self.record_btn.config(text="🛑 Stop Recording", bg="#ff5722")
    
    def process_recording(self):
        """Process recorded audio (runs in background thread)."""
        # Calculate duration
        duration = time.time() - self.recording_start_time if self.recording_start_time else 0
        
        # Stop recording and get audio
        audio_data = self.recorder.stop_recording()
        
        if len(audio_data) == 0:
            self.root.after(0, lambda: self.status_label.config(
                text="Status: No audio recorded",
                fg="#f44336"
            ))
            self.root.after(2000, lambda: self.status_label.config(
                text="Status: Idle",
                fg="#2e7d32"
            ))
            return
        
        # Transcribe
        text = self.transcriber.transcribe(audio_data)
        
        if not text:
            self.root.after(0, lambda: self.status_label.config(
                text="Status: No text transcribed",
                fg="#f44336"
            ))
            self.root.after(2000, lambda: self.status_label.config(
                text="Status: Idle",
                fg="#2e7d32"
            ))
            return
        
        # Save to database
        self.db.add_transcription(text, duration)
        
        # Get stored cursor position and type text
        stored_pos = self.cursor_tracker.get_stored_position()
        if stored_pos:
            self.typer.type_text(text, click_position=stored_pos)
        else:
            self.typer.type_text(text)
        
        # Update UI
        self.root.after(0, self.refresh_history)
        self.root.after(0, lambda: self.status_label.config(
            text="Status: Idle",
            fg="#2e7d32"
        ))
    
    def refresh_history(self):
        """Refresh the history display."""
        # Clear current history
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        # Get all transcriptions
        transcriptions = self.db.get_all_transcriptions()
        
        # Update count label
        self.history_count_label.config(
            text=f"📝 Transcription History ({len(transcriptions)} items)"
        )
        
        # Display each transcription
        for idx, (trans_id, timestamp, text, duration) in enumerate(transcriptions):
            # Container for each item
            item_frame = tk.Frame(
                self.history_frame,
                bg="#f9f9f9" if idx % 2 == 0 else "white",
                padx=10,
                pady=8
            )
            item_frame.pack(fill=tk.X, pady=2)
            
            # Timestamp and text
            info_frame = tk.Frame(item_frame, bg=item_frame["bg"])
            info_frame.pack(fill=tk.X, side=tk.TOP)
            
            time_label = tk.Label(
                info_frame,
                text=timestamp,
                font=("Arial", 9),
                fg="#666",
                bg=item_frame["bg"]
            )
            time_label.pack(side=tk.LEFT)
            
            if duration:
                duration_label = tk.Label(
                    info_frame,
                    text=f"({duration:.1f}s)",
                    font=("Arial", 8),
                    fg="#999",
                    bg=item_frame["bg"]
                )
                duration_label.pack(side=tk.LEFT, padx=5)
            
            # Text content
            text_label = tk.Label(
                item_frame,
                text=f'"{text}"',
                font=("Arial", 10),
                wraplength=550,
                justify=tk.LEFT,
                bg=item_frame["bg"]
            )
            text_label.pack(fill=tk.X, pady=(5, 5))
            
            # Buttons
            btn_frame = tk.Frame(item_frame, bg=item_frame["bg"])
            btn_frame.pack(fill=tk.X)
            
            copy_btn = tk.Button(
                btn_frame,
                text="📋 Copy",
                command=lambda t=text: self.copy_to_clipboard(t),
                font=("Arial", 8),
                bg="#2196f3",
                fg="white",
                padx=10,
                pady=3
            )
            copy_btn.pack(side=tk.LEFT, padx=2)
            
            delete_btn = tk.Button(
                btn_frame,
                text="🗑️ Delete",
                command=lambda tid=trans_id: self.delete_item(tid),
                font=("Arial", 8),
                bg="#ff5722",
                fg="white",
                padx=10,
                pady=3
            )
            delete_btn.pack(side=tk.LEFT, padx=2)
    
    def copy_to_clipboard(self, text: str):
        """Copy text to clipboard."""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_label.config(text="Status: Copied to clipboard!", fg="#2196f3")
        self.root.after(2000, lambda: self.status_label.config(
            text="Status: Idle",
            fg="#2e7d32"
        ))
    
    def delete_item(self, transcription_id: int):
        """Delete a specific transcription."""
        if messagebox.askyesno("Confirm Delete", "Delete this transcription?"):
            self.db.delete_transcription(transcription_id)
            self.refresh_history()
    
    def clear_all_history(self):
        """Clear all history."""
        if messagebox.askyesno("Confirm Clear All", "Delete ALL transcription history?"):
            self.db.clear_all()
            self.refresh_history()
    
    def update_status(self):
        """Update status periodically."""
        # This can be extended to show more real-time info
        self.root.after(100, self.update_status)
    
    def on_closing(self):
        """Handle window close event."""
        keyboard.unhook_all()
        self.root.destroy()


def main():
    """Main entry point for GUI application."""
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()

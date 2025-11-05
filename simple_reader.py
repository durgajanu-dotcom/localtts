import tkinter as tk
from tkinter import ttk, scrolledtext
import pyttsx3
import threading
import time

class SimpleTTS:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple TTS Reader")
        self.root.geometry("800x600")
        
        # Initialize state
        self.engine = None
        self.speaking = False
        self.current_word = None
        self.speech_thread = None
        
        # Create GUI
        self.create_ui()
        self.initialize_engine()
        
    def create_ui(self):
        # Text area with highlighting
        self.text_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=("Arial", 12),
            height=20
        )
        self.text_area.pack(expand=True, fill="both", padx=10, pady=5)
        self.text_area.tag_configure("highlight", background="yellow")
        
        # Simple controls
        controls = ttk.Frame(self.root)
        controls.pack(pady=10)
        
        self.play_button = ttk.Button(
            controls,
            text="Read",
            command=self.toggle_speech,
            width=20
        )
        self.play_button.pack(pady=5)
        
        self.status_var = tk.StringVar(value="Ready")
        status = ttk.Label(self.root, textvariable=self.status_var)
        status.pack(pady=5)
        
    def initialize_engine(self):
        """Initialize or reinitialize the TTS engine with complete cleanup"""
        try:
            # Stop and cleanup existing engine
            self.cleanup_engine()
                
            # Create new engine instance
            self.engine = pyttsx3.init()
            
            # Reset all properties
            self.engine.setProperty("rate", 150)
            
            # Try to find and set a female voice
            voices = self.engine.getProperty("voices")
            for voice in voices:
                if any(name in voice.name.lower() for name in ["zira", "microsoft", "female"]):
                    self.engine.setProperty("voice", voice.id)
                    break
                    
            # Connect word callback
            self.engine.connect("started-word", self.on_word)
            
            self.status_var.set("Ready")
            self.play_button.config(state="normal")
            
        except Exception as e:
            self.status_var.set(f"Error initializing: {e}")
            self.play_button.config(state="disabled")
            
    def cleanup_engine(self):
        """Clean up the engine completely"""
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass
            try:
                self.engine.endLoop()
            except:
                pass
            finally:
                del self.engine
                self.engine = None
                # Small delay to ensure cleanup
                time.sleep(0.1)
    
    def on_word(self, name, location, length):
        """Highlight the current word being spoken"""
        if not self.speaking:
            return
            
        try:
            # Remove previous highlight
            self.text_area.tag_remove("highlight", "1.0", tk.END)
            
            # Get text position
            text = self.text_area.get("1.0", tk.END)
            
            # Find word position
            row = 1
            col = 0
            count = 0
            
            # Count characters to find the word position
            for i, char in enumerate(text):
                if i == location:
                    col = count
                    break
                if char == "\n":
                    row += 1
                    count = 0
                else:
                    count += 1
            
            # Calculate positions for highlighting
            start = f"{row}.{col}"
            end = f"{row}.{col + length}"
            
            # Apply highlight
            self.text_area.tag_add("highlight", start, end)
            
            # Ensure word is visible
            self.text_area.see(start)
            
        except Exception:
            pass  # Ignore highlight errors
            
    def speak_text(self):
        """Thread function for speaking text"""
        try:
            if not self.speaking:
                return
                
            text = self.text_area.get("1.0", tk.END).strip()
            if text:
                self.engine.say(text)
                self.engine.runAndWait()
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {e}"))
        finally:
            self.root.after(0, self.speech_finished)
    
    def speech_finished(self):
        """Reset state after speech finishes"""
        self.speaking = False
        self.speech_thread = None
        self.play_button.config(text="Read")
        self.status_var.set("Ready")
        self.text_area.tag_remove("highlight", "1.0", tk.END)
        # Complete cleanup and reinitialize
        self.initialize_engine()
    
    def toggle_speech(self):
        """Start or stop speech"""
        if not self.speaking:
            text = self.text_area.get("1.0", tk.END).strip()
            if text:
                # Initialize fresh engine instance before starting
                self.initialize_engine()
                self.speaking = True
                self.play_button.config(text="Stop")
                self.status_var.set("Reading...")
                
                # Start speech in thread
                self.speech_thread = threading.Thread(target=self.speak_text, daemon=True)
                self.speech_thread.start()
        else:
            # Stop speech
            self.speaking = False
            self.cleanup_engine()
            self.speech_finished()
            
    def __del__(self):
        """Cleanup on exit"""
        self.cleanup_engine()
            
def main():
    root = tk.Tk()
    app = SimpleTTS(root)
    root.mainloop()

if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import filedialog, messagebox
import time

class DangerousWritingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The non-sense Writing App")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e1e")

        # Configuration
        self.TIMEOUT_SECONDS = 5.0
        self.last_typed_time = None
        self.is_active = False
        self.timer_job = None

        self._setup_ui()

    def _setup_ui(self):
        # Top control/status bar
        top_frame = tk.Frame(self.root, bg="#1e1e1e", pady=10, padx=20)
        top_frame.pack(fill=tk.X)

        self.status_label = tk.Label(
            top_frame,
            text="Start typing...",
            font=("Helvetica", 12, "bold"),
            fg="#888888",
            bg="#1e1e1e"
        )
        self.status_label.pack(side=tk.LEFT)

        self.word_count_label = tk.Label(
            top_frame,
            text="Words: 0",
            font=("Helvetica", 11),
            fg="#888888",
            bg="#1e1e1e"
        )
        self.word_count_label.pack(side=tk.RIGHT, padx=(15, 0))

        self.save_btn = tk.Button(
            top_frame,
            text="Save Work",
            command=self.save_file,
            bg="#333333",
            fg="#ffffff",
            activebackground="#444444",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=10,
            pady=3
        )
        self.save_btn.pack(side=tk.RIGHT)

        # progress bar 
        self.progress_canvas = tk.Canvas(
            self.root,
            height=6,
            bg="#2d2d2d",
            highlightthickness=0
        )
        self.progress_canvas.pack(fill=tk.X, padx=20)
        self.progress_bar = self.progress_canvas.create_rectangle(
            0, 0, 800, 6, fill="#4caf50", width=0
        )

        # Main Text Area
        self.text_area = tk.Text(
            self.root,
            font=("Georgia", 15),
            bg="#1e1e1e",
            fg="#e0e0e0",
            insertbackground="#ffffff",
            relief=tk.FLAT,
            wrap=tk.WORD,
            padx=30,
            pady=20,
            undo=False  # Disable Ctrl+Z to prevent cheating
        )
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.text_area.focus_set()

        # Bind key press events
        self.text_area.bind("<KeyPress>", self.on_key_press)

    def on_key_press(self, event):
        # Ignore modifier keys (Shift, Ctrl, Alt, ...)
        ignored_keys = {
            "Shift_L", "Shift_R", "Control_L", "Control_R",
            "Alt_L", "Alt_R", "Caps_Lock", "Tab", "Escape",
            "Up", "Down", "Left", "Right"
        }
        if event.keysym in ignored_keys:
            return

        self.last_typed_time = time.time()

        if not self.is_active:
            self.is_active = True
            self.update_timer()

        # Schedule word count update slightly after keystroke is processed
        self.root.after(10, self.update_word_count)

    def update_timer(self):
        if not self.is_active:
            return

        elapsed = time.time() - self.last_typed_time
        remaining = max(0.0, self.TIMEOUT_SECONDS - elapsed)

        if remaining <= 0:
            self.wipe_progress()
            return

        # Update status text
        self.status_label.config(text=f"Time remaining: {remaining:.1f}s")

        # Update progress bar width and color based on urgency
        canvas_width = self.progress_canvas.winfo_width()
        bar_width = (remaining / self.TIMEOUT_SECONDS) * canvas_width
        self.progress_canvas.coords(self.progress_bar, 0, 0, bar_width, 6)

        if remaining > 3.0:
            color = "#4caf50"  # Green
            text_fg = "#e0e0e0"
        elif remaining > 1.5:
            color = "#ff9800"  # Orange warning
            text_fg = "#ffcc80"
        else:
            color = "#f44336"  # Red danger
            text_fg = "#ff8a80"

        self.progress_canvas.itemconfig(self.progress_bar, fill=color)
        self.status_label.config(fg=color)
        self.text_area.config(fg=text_fg)

        # Run loop every 50ms for smooth countdown
        self.timer_job = self.root.after(50, self.update_timer)

    def wipe_progress(self):
        self.is_active = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)

        # Delete all text
        self.text_area.delete("1.0", tk.END)
        self.text_area.config(fg="#e0e0e0")
        self.update_word_count()

        # Reset UI indicators
        self.status_label.config(
            text="TIME'S UP! All progress lost. Type to restart.",
            fg="#f44336"
        )
        self.progress_canvas.coords(self.progress_bar, 0, 0, 0, 6)

    def update_word_count(self):
        content = self.text_area.get("1.0", tk.END).strip()
        words = len(content.split()) if content else 0
        self.word_count_label.config(text=f"Words: {words}")

    def save_file(self):
        # Pause timer while save dialog is open
        was_active = self.is_active
        self.is_active = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)

        content = self.text_area.get("1.0", tk.END).strip()
        if not content:
            messagebox.showinfo("Empty", "Nothing to save!")
        else:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("Markdown", "*.md"), ("All Files", "*.*")]
            )
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                self.status_label.config(text="Saved! Type to resume.", fg="#4caf50")

        # Reset clock so user gets a fresh 5 seconds upon returning
        if was_active:
            self.last_typed_time = time.time()
            self.is_active = True
            self.update_timer()

if __name__ == "__main__":
    root = tk.Tk()
    app = DangerousWritingApp(root)
    root.mainloop()

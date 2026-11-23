import tkinter as tk
from tkinter import ttk
import time
import random


class TypingSpeedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("760x540")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self.sample_texts = [
            "The quick brown fox jumps over the lazy dog while the sun sets behind the distant mountains.",
            "Python is a high-level, general-purpose programming language whose design philosophy emphasizes code readability.",
            "Practice makes permanent, so focus on accuracy first and let your typing speed develop naturally over time.",
            "Algorithms and data structures form the core foundation of efficient software engineering and problem solving.",
            "A journey of a thousand miles begins with a single step, and every keystroke brings you closer to mastery.",
            "Clean code always looks like it was written by someone who cares deeply about clarity and maintainability.",
            "Consistent daily habits compound over months and years to produce remarkable improvements in skill and focus.",
        ]

        self.target_text = ""
        self.start_time = None
        self.timer_running = False
        self.timer_job = None
        self.test_completed = False

        self.setup_styles()
        self.build_ui()
        self.reset_test()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Accent.TButton",
            font=("Segoe UI", 11, "bold"),
            foreground="#1e1e2e",
            background="#89b4fa",
            padding=(16, 8),
            borderwidth=0,
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#74c7ec"), ("pressed", "#b4befe")],
        )

    def build_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#1e1e2e")
        header_frame.pack(pady=(24, 10), padx=32, fill="x")

        title_label = tk.Label(
            header_frame,
            text="Typing Speed Test",
            font=("Segoe UI", 22, "bold"),
            fg="#cdd6f4",
            bg="#1e1e2e",
        )
        title_label.pack(side="left")

        subtitle_label = tk.Label(
            header_frame,
            text="Start typing below to begin the timer",
            font=("Segoe UI", 10),
            fg="#a6adc8",
            bg="#1e1e2e",
        )
        subtitle_label.pack(side="right", anchor="s", pady=4)

        # Live Stats Bar
        stats_frame = tk.Frame(self.root, bg="#313244", bd=0, highlightthickness=1, highlightbackground="#45475a")
        stats_frame.pack(pady=10, padx=32, fill="x")

        for i in range(3):
            stats_frame.columnconfigure(i, weight=1)

        self.wpm_var = tk.StringVar(value="0")
        self.acc_var = tk.StringVar(value="100%")
        self.time_var = tk.StringVar(value="0.0s")

        self._create_stat_card(stats_frame, 0, "WPM", self.wpm_var, "#a6e3a1")
        self._create_stat_card(stats_frame, 1, "ACCURACY", self.acc_var, "#89b4fa")
        self._create_stat_card(stats_frame, 2, "TIME", self.time_var, "#f9e2af")

        # Prompt Display Box (Read-only Text widget for per-character color highlighting)
        prompt_label = tk.Label(
            self.root,
            text="SAMPLE TEXT",
            font=("Segoe UI", 9, "bold"),
            fg="#a6adc8",
            bg="#1e1e2e",
        )
        prompt_label.pack(anchor="w", padx=32, pady=(12, 4))

        self.prompt_display = tk.Text(
            self.root,
            height=4,
            font=("Consolas", 14),
            bg="#181825",
            fg="#cdd6f4",
            wrap="word",
            padx=16,
            pady=14,
            bd=0,
            highlightthickness=1,
            highlightbackground="#45475a",
            cursor="arrow",
        )
        self.prompt_display.pack(padx=32, fill="x")
        self.prompt_display.config(state="disabled")

        # Highlighting tags
        self.prompt_display.tag_configure("correct", foreground="#a6e3a1")
        self.prompt_display.tag_configure("incorrect", foreground="#f38ba8", background="#3b222c")
        self.prompt_display.tag_configure("current", underline=True, foreground="#f9e2af")
        self.prompt_display.tag_configure("remaining", foreground="#9399b2")

        # User Input Box
        input_label = tk.Label(
            self.root,
            text="YOUR INPUT",
            font=("Segoe UI", 9, "bold"),
            fg="#a6adc8",
            bg="#1e1e2e",
        )
        input_label.pack(anchor="w", padx=32, pady=(16, 4))

        self.input_box = tk.Text(
            self.root,
            height=4,
            font=("Consolas", 14),
            bg="#313244",
            fg="#cdd6f4",
            insertbackground="#cdd6f4",
            wrap="word",
            padx=16,
            pady=14,
            bd=0,
            highlightthickness=2,
            highlightbackground="#45475a",
            highlightcolor="#89b4fa",
        )
        self.input_box.pack(padx=32, fill="x")
        self.input_box.bind("<KeyRelease>", self.on_key_release)
        self.input_box.bind("<Return>", self.prevent_newline)

        # Status & Controls Footer
        footer_frame = tk.Frame(self.root, bg="#1e1e2e")
        footer_frame.pack(pady=(20, 16), padx=32, fill="x")

        self.status_var = tk.StringVar(value="Ready when you are.")
        self.status_label = tk.Label(
            footer_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 11, "bold"),
            fg="#a6e3a1",
            bg="#1e1e2e",
        )
        self.status_label.pack(side="left")

        reset_btn = ttk.Button(
            footer_frame,
            text="New Passage (Esc)",
            style="Accent.TButton",
            command=self.reset_test,
        )
        reset_btn.pack(side="right")

        self.root.bind("<Escape>", lambda e: self.reset_test())

    def _create_stat_card(self, parent, col, title, textvariable, color):
        frame = tk.Frame(parent, bg="#313244", pady=12)
        frame.grid(row=0, column=col, sticky="nsew")

        val_lbl = tk.Label(
            frame,
            textvariable=textvariable,
            font=("Segoe UI", 22, "bold"),
            fg=color,
            bg="#313244",
        )
        val_lbl.pack()

        title_lbl = tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 9, "bold"),
            fg="#a6adc8",
            bg="#313244",
        )
        title_lbl.pack()

    def prevent_newline(self, event):
        return "break"

    def reset_test(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        self.start_time = None
        self.timer_running = False
        self.test_completed = False

        # Pick a different passage than the current one
        choices = [t for t in self.sample_texts if t != self.target_text]
        self.target_text = random.choice(choices)

        self.wpm_var.set("0")
        self.acc_var.set("100%")
        self.time_var.set("0.0s")
        self.status_var.set("Ready when you are.")
        self.status_label.config(fg="#a6adc8")

        self.input_box.config(state="normal")
        self.input_box.delete("1.0", tk.END)
        self.input_box.focus_set()

        self.render_prompt("")

    def render_prompt(self, typed_text):
        self.prompt_display.config(state="normal")
        self.prompt_display.delete("1.0", tk.END)

        for i, target_char in enumerate(self.target_text):
            if i < len(typed_text):
                tag = "correct" if typed_text[i] == target_char else "incorrect"
            elif i == len(typed_text):
                tag = "current"
            else:
                tag = "remaining"
            self.prompt_display.insert(tk.END, target_char, tag)

        self.prompt_display.config(state="disabled")

    def update_timer(self):
        if not self.timer_running or self.test_completed:
            return

        elapsed = time.perf_counter() - self.start_time
        self.time_var.set(f"{elapsed:.1f}s")

        typed = self.input_box.get("1.0", "end-1c")
        self.calculate_metrics(typed, elapsed)

        self.timer_job = self.root.after(100, self.update_timer)

    def calculate_metrics(self, typed, elapsed):
        if elapsed <= 0 or not typed:
            self.wpm_var.set("0")
            self.acc_var.set("100%")
            return

        correct_chars = sum(
            1 for i, c in enumerate(typed) if i < len(self.target_text) and c == self.target_text[i]
        )

        # Standard WPM formula: (correct characters / 5) / minutes elapsed
        minutes = elapsed / 60.0
        wpm = int(round((correct_chars / 5.0) / minutes))
        accuracy = (correct_chars / len(typed)) * 100.0

        self.wpm_var.set(str(wpm))
        self.acc_var.set(f"{accuracy:.0f}%")

    def on_key_release(self, event):
        if self.test_completed:
            return

        # Ignore standalone modifier keys
        if event.keysym in ("Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R", "Caps_Lock", "Escape"):
            return

        typed = self.input_box.get("1.0", "end-1c")

        # Start timer on first actual character typed
        if not self.timer_running and len(typed) > 0:
            self.start_time = time.perf_counter()
            self.timer_running = True
            self.status_var.set("Keep going...")
            self.status_label.config(fg="#89b4fa")
            self.update_timer()

        self.render_prompt(typed)

        # Check completion when typed length reaches target length
        if len(typed) >= len(self.target_text):
            self.finish_test(typed)

    def finish_test(self, typed):
        self.test_completed = True
        self.timer_running = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        elapsed = time.perf_counter() - self.start_time
        self.time_var.set(f"{elapsed:.2f}s")
        self.calculate_metrics(typed, elapsed)

        self.input_box.config(state="disabled")
        self.status_var.set(f"Complete! Final Speed: {self.wpm_var.get()} WPM at {self.acc_var.get()} accuracy.")
        self.status_label.config(fg="#a6e3a1")


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedApp(root)
    root.mainloop()
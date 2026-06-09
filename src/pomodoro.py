import tkinter as tk
import winsound

FOCUS_SEC = 25 * 60
STRETCH_SEC = 3 * 60
REVIEW_SEC = 5 * 60
LONG_BREAK_SEC = 15 * 60
DOT_COUNT = 4
MODE_ORDER = ["focus", "stretch", "review", "long_break"]

BG = "#fff4dc"              # Brighter warm cream background
SURFACE = "#fff0d0"         # Brighter cream surface
TEXT_PRIMARY = "#4a3f35"    # Deep brown text (soft contrast)
TEXT_SECONDARY = "#8b7d6b"  # Gray-brown secondary text
RING_TRACK = "#f5e6c8"      # Brighter progress ring track
DOT_EMPTY = "#ecdcbb"       # Brighter empty dots

# Per-mode accent
MODE_COLORS = {
    "focus":      "#d4845c",  # Warm orange-brown (work)
    "stretch":    "#8ab88f",  # Soft mint green (activity)
    "review":     "#e8b563",  # Soft golden (review)
    "long_break": "#9ba8c7",  # Soft lavender blue (rest)
}
MODE_LABELS = {
    "focus":      "FOCUS",
    "stretch":    "STRETCH",
    "review":     "REVIEW",
    "long_break": "LONG BREAK",
}
MODE_SUBTITLES = {
    "focus":      "Deep work",
    "stretch":    "Stand up & move",
    "review":     "Check your progress",
    "long_break": "Take a real rest",
}
MODE_DOT_LABELS = {
    "focus":      "FOCUS",
    "stretch":    "MOVE",
    "review":     "CHECK",
    "long_break": "REST",
}

BTN_START = "#d4845c"
BTN_PAUSE = "#e8b563"
BTN_RESET = "#a89680"

# 4 dots are mode indicators, not focus-count indicators:
#   FOCUS · STRETCH · REVIEW · LONG BREAK
# The active mode dot uses that mode's color. Focus cycle progress is shown in
# the center text, e.g. "Focus 2/4".


class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, bg_color, width=90, height=34, radius=17):
        super().__init__(parent, width=width, height=height,
                         bg=BG, highlightthickness=0, cursor="hand2")
        self.command = command
        self.bg_color = bg_color
        self.radius = radius
        self.width = width
        self.height = height
        self.text = text
        self._draw(bg_color)
        self.bind("<Button-1>", lambda e: command())
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _draw(self, color):
        self.delete("all")
        r = self.radius
        w, h = self.width, self.height
        self.create_arc(0, 0, 2*r, 2*r, start=90, extent=90, fill=color, outline="")
        self.create_arc(w-2*r, 0, w, 2*r, start=0, extent=90, fill=color, outline="")
        self.create_arc(0, h-2*r, 2*r, h, start=180, extent=90, fill=color, outline="")
        self.create_arc(w-2*r, h-2*r, w, h, start=270, extent=90, fill=color, outline="")
        self.create_rectangle(r, 0, w-r, h, fill=color, outline="")
        self.create_rectangle(0, r, w, h-r, fill=color, outline="")
        self.create_text(w/2, h/2, text=self.text, fill="white",
                         font=("Segoe UI", 10, "bold"))

    def _on_enter(self, e):
        r, g, b = self.winfo_rgb(self.bg_color)
        r, g, b = r//256, g//256, b//256
        r = min(255, int(r * 1.15))
        g = min(255, int(g * 1.15))
        b = min(255, int(b * 1.15))
        self._draw(f"#{r:02x}{g:02x}{b:02x}")

    def _on_leave(self, e):
        self._draw(self.bg_color)


class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro")
        self.root.geometry("320x490")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.root.attributes("-topmost", True)

        self.mode = "focus"
        self.seconds = FOCUS_SEC
        self.total_seconds = FOCUS_SEC
        self.running = False
        self.focus_done = 0  # 0–DOT_COUNT focus sessions completed in this cycle
        self.timer_id = None

        self._build_ui()

    # ── UI construction ────────────────────────────────────────────

    def _build_ui(self):
        # Title
        tk.Label(self.root, text="Pomodoro", font=("Segoe UI", 16, "bold"),
                 fg=TEXT_PRIMARY, bg=BG).pack(pady=(24, 2))

        # Mode label
        self.mode_label = tk.Label(self.root, text="FOCUS", font=("Segoe UI", 12, "bold"),
                                   fg=MODE_COLORS["focus"], bg=BG)
        self.mode_label.pack()

        # Subtitle
        self.subtitle_label = tk.Label(self.root, text="Deep work", font=("Segoe UI", 9),
                                       fg=TEXT_SECONDARY, bg=BG)
        self.subtitle_label.pack(pady=(0, 4))

        # Canvas ring
        self.canvas_size = 220
        self.canvas = tk.Canvas(self.root, width=self.canvas_size,
                                height=self.canvas_size,
                                bg=BG, highlightthickness=0)
        self.canvas.pack(pady=(4, 0))

        self.timer_text = self.canvas.create_text(
            self.canvas_size/2, self.canvas_size/2 - 6,
            text=self._fmt(self.seconds), fill=TEXT_PRIMARY,
            font=("Consolas", 36, "bold")
        )
        self.progress_text = self.canvas.create_text(
            self.canvas_size/2, self.canvas_size/2 + 28,
            text="", fill=TEXT_SECONDARY, font=("Segoe UI", 9)
        )
        self._draw_ring(0)

        # Dot row
        dot_frame = tk.Frame(self.root, bg=BG)
        dot_frame.pack(pady=(14, 2))

        self.dot_labels = []  # text under each dot
        for i in range(DOT_COUNT):
            col = tk.Frame(dot_frame, bg=BG)
            col.pack(side="left", padx=10)

            c = tk.Canvas(col, width=18, height=18, bg=BG, highlightthickness=0)
            c.pack()
            c.create_oval(2, 2, 18, 18, fill=DOT_EMPTY, outline="")

            lbl = tk.Label(col, text=f"F{i+1}", font=("Segoe UI", 7),
                           fg=TEXT_SECONDARY, bg=BG)
            lbl.pack()

            self.dot_labels.append((c, lbl))

        self._update_dots()

        # Buttons — 2x2 grid (Start/Pause merged, 3 buttons total)
        btn_grid = tk.Frame(self.root, bg=BG)
        btn_grid.pack(pady=(12, 0))

        self.play_btn = RoundedButton(btn_grid, "Start", self.start, BTN_START, width=120)
        self.play_btn.grid(row=0, column=0, columnspan=2, padx=5, pady=4)

        self.reset_btn = RoundedButton(btn_grid, "Reset", self.reset, BTN_RESET)
        self.reset_btn.grid(row=1, column=0, padx=5, pady=4)

        self.skip_btn = RoundedButton(btn_grid, "Skip", self.skip, BTN_RESET)
        self.skip_btn.grid(row=1, column=1, padx=5, pady=4)

        # Always on top
        self.topmost_var = tk.BooleanVar(value=True)
        cb = tk.Checkbutton(self.root, text="Always on top",
                            variable=self.topmost_var,
                            command=self._toggle_topmost,
                            fg=TEXT_SECONDARY, bg=BG,
                            selectcolor=SURFACE, activebackground=BG,
                            activeforeground=TEXT_PRIMARY,
                            font=("Segoe UI", 8))
        cb.pack(pady=(14, 0))

    # ── Display helpers ────────────────────────────────────────────

    def _fmt(self, s):
        return f"{s // 60:02d}:{s % 60:02d}"

    def _toggle_topmost(self):
        self.root.attributes("-topmost", self.topmost_var.get())

    def _accent_color(self):
        return MODE_COLORS.get(self.mode, MODE_COLORS["focus"])

    def _draw_ring(self, fraction):
        self.canvas.delete("ring")
        cx = cy = self.canvas_size / 2
        r = 85
        sw = 8

        self.canvas.create_oval(cx - r - sw/2, cy - r - sw/2,
                                cx + r + sw/2, cy + r + sw/2,
                                outline=RING_TRACK, width=sw, tags="ring")
        if fraction > 0:
            extent = -fraction * 360
            self.canvas.create_arc(cx - r, cy - r, cx + r, cy + r,
                                   start=90, extent=extent,
                                   outline=self._accent_color(),
                                   width=sw, style="arc", tags="ring")

    def _update_ring(self):
        fraction = 1 - (self.seconds / self.total_seconds) if self.total_seconds > 0 else 1
        self._draw_ring(fraction)

    def _update_dots(self):
        """Dots show FOCUS progress (0-4), color indicates current mode."""
        current_color = MODE_COLORS[self.mode]

        for i, (canvas, label) in enumerate(self.dot_labels):
            canvas.delete("all")

            if i < self.focus_done:
                # Completed focus — solid fill with current mode color
                canvas.create_oval(2, 2, 18, 18, fill=current_color, outline="")
                label.config(fg=current_color)
            elif self.mode == "focus" and i == self.focus_done:
                # Currently working on this focus — ring outline
                canvas.create_oval(2, 2, 18, 18, fill=DOT_EMPTY, outline="")
                canvas.create_oval(4, 4, 16, 16, outline=current_color, width=2)
                label.config(fg=current_color)
            else:
                # Future focus — empty
                canvas.create_oval(2, 2, 18, 18, fill=DOT_EMPTY, outline="")
                label.config(fg=TEXT_SECONDARY)

    def _update_display(self):
        self.canvas.itemconfig(self.timer_text, text=self._fmt(self.seconds))
        self._update_ring()
        done_min = (self.total_seconds - self.seconds) // 60
        total_min = self.total_seconds // 60
        self.canvas.itemconfig(self.progress_text, text=f"{done_min}/{total_min} min")

        color = self._accent_color()
        self.mode_label.config(text=MODE_LABELS[self.mode], fg=color)
        self.subtitle_label.config(text=MODE_SUBTITLES[self.mode])
        self._update_dots()

        # Update play button text based on state
        if self.running:
            self.play_btn.text = "Pause"
        elif self.seconds < self.total_seconds:
            self.play_btn.text = "Resume"
        else:
            self.play_btn.text = "Start"
        self.play_btn._draw(self.play_btn.bg_color)

    # ── Timer engine ───────────────────────────────────────────────

    def _tick(self):
        if not self.running:
            return
        if self.seconds > 0:
            self.seconds -= 1
            self._update_display()
            self.timer_id = self.root.after(1000, self._tick)
        else:
            self._on_complete()

    def _on_complete(self):
        self.running = False
        import threading

        def beep_beep():
            # Gentle reminder: C5-E5 (major third)
            winsound.Beep(523, 200)  # C5 (do)
            winsound.Beep(659, 200)  # E5 (mi)

        threading.Thread(target=beep_beep, daemon=True).start()
        self._advance()

    def _advance(self):
        """Move to the next mode in the cycle."""
        if self.mode == "focus":
            self.focus_done += 1
            self._update_dots()

            if self.focus_done == DOT_COUNT:
                self.mode = "long_break"
                self.seconds = LONG_BREAK_SEC
            elif self.focus_done == 2:
                # Mid-cycle review
                self.mode = "review"
                self.seconds = REVIEW_SEC
            else:
                self.mode = "stretch"
                self.seconds = STRETCH_SEC
        else:
            # Any break → go back to focus; if cycle was complete, reset dots
            if self.mode == "long_break":
                self.focus_done = 0
                self._update_dots()
            self.mode = "focus"
            self.seconds = FOCUS_SEC

        self.total_seconds = self.seconds
        self._update_display()

    # ── Button actions ─────────────────────────────────────────────

    def start(self):
        """Toggle between start/pause/resume."""
        if self.running:
            # Currently running → pause
            self.running = False
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            self._update_display()
        else:
            # Currently paused or not started → start/resume
            self.running = True
            if self.seconds == self.total_seconds:
                # Fresh start, not resuming
                pass
            self._update_display()
            self._tick()

    def pause(self):
        """Kept for backwards compatibility, just calls start() to toggle."""
        self.start()

    def reset(self):
        """Reset current mode timer to initial value, don't change mode or progress."""
        self.running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        # Reset to current mode's initial duration
        mode_durations = {
            "focus": FOCUS_SEC,
            "stretch": STRETCH_SEC,
            "review": REVIEW_SEC,
            "long_break": LONG_BREAK_SEC,
        }
        self.seconds = mode_durations[self.mode]
        self.total_seconds = self.seconds
        self._update_display()

    def skip(self):
        self.running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        # Play gentle reminder sound
        import threading

        def beep_beep():
            winsound.Beep(523, 200)  # C5 (do)
            winsound.Beep(659, 200)  # E5 (mi)

        threading.Thread(target=beep_beep, daemon=True).start()

        if self.mode == "focus":
            # Skip work → count it as done, go to the break that would follow
            self.focus_done += 1
            if self.focus_done == DOT_COUNT:
                self.mode = "long_break"
                self.seconds = LONG_BREAK_SEC
            elif self.focus_done == 2:
                self.mode = "review"
                self.seconds = REVIEW_SEC
            else:
                self.mode = "stretch"
                self.seconds = STRETCH_SEC
        else:
            # Skip break → go to next focus
            if self.mode == "long_break":
                self.focus_done = 0
            self.mode = "focus"
            self.seconds = FOCUS_SEC

        self.total_seconds = self.seconds
        self._update_dots()
        self._update_display()


def main():
    root = tk.Tk()
    PomodoroTimer(root)
    root.mainloop()


if __name__ == "__main__":
    main()

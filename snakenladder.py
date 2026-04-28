import tkinter as tk
from tkinter import messagebox
import random
import math

# ─── Game Data ────────────────────────────────────────────────────────────────

SNAKES = {
    97: 78, 95: 56, 88: 24, 62: 19, 48: 26, 36: 6, 32: 10, 17: 4
}

LADDERS = {
    4: 14, 9: 31, 20: 38, 28: 84, 40: 59, 51: 67, 63: 81, 71: 91
}

BOARD_SIZE     = 10
CELL_SIZE      = 62
BOARD_OFFSET_X = 20
BOARD_OFFSET_Y = 20
BOARD_PX       = BOARD_SIZE * CELL_SIZE   # 620
BOARD_PY       = BOARD_SIZE * CELL_SIZE   # 620

PLAYER_COLORS  = ["#FF4D6D", "#4361EE"]
PLAYER_NAMES   = ["Player 1", "Player 2"]
PLAYER_ICONS   = ["★", "♦"]

BG_COLOR       = "#0D1B2A"
BOARD_LIGHT    = "#1E3A5F"
BOARD_DARK     = "#16304F"
TEXT_COLOR      = "#E0E7FF"
ACCENT         = "#4CC9F0"
LADDER_COLOR   = "#06D6A0"
SNAKE_COLOR    = "#FF6B6B"
DICE_BG        = "#1E3A5F"
PANEL_BG       = "#0D1B2A"

# ─── Helpers ──────────────────────────────────────────────────────────────────

def cell_to_xy(cell: int):
    """Return (col, row) 0-indexed from bottom-left for a 1-based cell number."""
    cell -= 1                           # 0-based
    row  = cell // BOARD_SIZE           # 0 = bottom row
    col  = cell  % BOARD_SIZE
    if row % 2 == 1:                    # odd rows go right-to-left
        col = BOARD_SIZE - 1 - col
    return col, row

def cell_center(cell: int):
    col, row = cell_to_xy(cell)
    x = BOARD_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
    y = BOARD_OFFSET_Y + (BOARD_SIZE - 1 - row) * CELL_SIZE + CELL_SIZE // 2
    return x, y

# ─── Main App ─────────────────────────────────────────────────────────────────

class SnakeLadderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎲 Snakes & Ladders")
        self.resizable(False, False)
        self.configure(bg=BG_COLOR)
        self._build_ui()
        self.new_game()

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # Left: board canvas
        canvas_w = BOARD_PX + BOARD_OFFSET_X * 2
        canvas_h = BOARD_PY + BOARD_OFFSET_Y * 2
        self.canvas = tk.Canvas(self, width=canvas_w, height=canvas_h,
                                bg=BG_COLOR, highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=(16, 8), pady=16)

        # Right: control panel
        panel = tk.Frame(self, bg=PANEL_BG, width=220)
        panel.grid(row=0, column=1, sticky="ns", padx=(8, 16), pady=16)
        panel.grid_propagate(False)
        self._build_panel(panel)

    def _build_panel(self, panel):
        pad = dict(padx=12, pady=6)

        tk.Label(panel, text="🎲 SNAKES &\n   LADDERS",
                 font=("Courier", 18, "bold"),
                 bg=PANEL_BG, fg=ACCENT).pack(pady=(20, 4))

        # Player info cards
        self.player_frames = []
        self.pos_labels    = []
        self.score_labels  = []
        for i in range(2):
            f = tk.Frame(panel, bg=PLAYER_COLORS[i], bd=0)
            f.pack(fill="x", **pad)

            tk.Label(f, text=f"{PLAYER_ICONS[i]} {PLAYER_NAMES[i]}",
                     font=("Courier", 12, "bold"),
                     bg=PLAYER_COLORS[i], fg="white").pack(anchor="w", padx=8, pady=(6, 0))

            pos = tk.Label(f, text="Position: 0",
                           font=("Courier", 10),
                           bg=PLAYER_COLORS[i], fg="white")
            pos.pack(anchor="w", padx=8)
            self.pos_labels.append(pos)

            sc = tk.Label(f, text="Wins: 0",
                          font=("Courier", 10),
                          bg=PLAYER_COLORS[i], fg="white")
            sc.pack(anchor="w", padx=8, pady=(0, 6))
            self.score_labels.append(sc)
            self.player_frames.append(f)

        # Dice display
        tk.Label(panel, text="DICE", font=("Courier", 10, "bold"),
                 bg=PANEL_BG, fg=TEXT_COLOR).pack(pady=(16, 0))
        self.dice_canvas = tk.Canvas(panel, width=80, height=80,
                                     bg=DICE_BG, highlightthickness=2,
                                     highlightbackground=ACCENT)
        self.dice_canvas.pack(pady=4)
        self._draw_dice(0)

        # Turn label
        self.turn_label = tk.Label(panel, text="",
                                   font=("Courier", 11, "bold"),
                                   bg=PANEL_BG, fg=ACCENT, wraplength=190,
                                   justify="center")
        self.turn_label.pack(pady=(10, 4))

        # Log box
        tk.Label(panel, text="LOG", font=("Courier", 10, "bold"),
                 bg=PANEL_BG, fg=TEXT_COLOR).pack()
        log_frame = tk.Frame(panel, bg=PANEL_BG)
        log_frame.pack(fill="both", expand=True, padx=12, pady=4)
        sb = tk.Scrollbar(log_frame)
        sb.pack(side="right", fill="y")
        self.log_box = tk.Text(log_frame, width=22, height=10,
                               font=("Courier", 9),
                               bg="#0A1628", fg=TEXT_COLOR,
                               yscrollcommand=sb.set,
                               state="disabled", bd=0, wrap="word")
        self.log_box.pack(side="left", fill="both", expand=True)
        sb.config(command=self.log_box.yview)

        # Buttons
        self.roll_btn = tk.Button(panel, text="🎲  ROLL DICE",
                                  font=("Courier", 13, "bold"),
                                  bg=ACCENT, fg=BG_COLOR,
                                  activebackground="#70D6FF",
                                  relief="flat", cursor="hand2",
                                  command=self.roll_dice)
        self.roll_btn.pack(fill="x", padx=12, pady=(8, 4))

        tk.Button(panel, text="↺  NEW GAME",
                  font=("Courier", 11),
                  bg="#344955", fg=TEXT_COLOR,
                  activebackground="#4A6572",
                  relief="flat", cursor="hand2",
                  command=self.new_game).pack(fill="x", padx=12, pady=(0, 16))

    # ── Game Logic ────────────────────────────────────────────────────────────

    def new_game(self):
        self.positions  = [0, 0]
        self.wins       = getattr(self, "wins", [0, 0])
        self.current    = 0
        self.game_over  = False
        self._clear_log()
        self._draw_board()
        self._draw_snakes_ladders()
        self._draw_players()
        self._highlight_current()
        self.roll_btn.config(state="normal")
        self.turn_label.config(text=f"{PLAYER_NAMES[0]}'s Turn")
        self._log(f"🎮 New game started!\n{PLAYER_NAMES[0]} goes first.")

    def roll_dice(self):
        if self.game_over:
            return
        self.roll_btn.config(state="disabled")
        self._animate_dice_roll(steps=10, callback=self._apply_roll)

    def _animate_dice_roll(self, steps, callback):
        if steps == 0:
            callback()
            return
        self._draw_dice(random.randint(1, 6))
        self.after(60, lambda: self._animate_dice_roll(steps - 1, callback))

    def _apply_roll(self):
        roll  = random.randint(1, 6)
        self._draw_dice(roll)
        p     = self.current
        old   = self.positions[p]
        new   = old + roll

        self._log(f"\n{PLAYER_ICONS[p]} {PLAYER_NAMES[p]} rolled {roll}")

        if new > 100:
            self._log(f"  Needs {100 - old} to win. Stay at {old}.")
            self._next_turn()
            return

        self.positions[p] = new
        self._log(f"  Moved {old} → {new}")

        # Check snake / ladder
        if new in SNAKES:
            dest = SNAKES[new]
            self._log(f"  🐍 Snake! {new} → {dest}")
            self.positions[p] = dest
        elif new in LADDERS:
            dest = LADDERS[new]
            self._log(f"  🪜 Ladder! {new} → {dest}")
            self.positions[p] = dest

        self._draw_board()
        self._draw_snakes_ladders()
        self._draw_players()
        self._update_pos_labels()

        if self.positions[p] == 100:
            self.game_over = True
            self.wins[p]  += 1
            self._update_score_labels()
            self._log(f"\n🏆 {PLAYER_NAMES[p]} WINS!")
            self.turn_label.config(text=f"🏆 {PLAYER_NAMES[p]} Wins!")
            self.after(300, lambda: messagebox.showinfo(
                "Game Over", f"🎉 {PLAYER_NAMES[p]} wins the game!\n\nScore:\n"
                             f"  {PLAYER_NAMES[0]}: {self.wins[0]} wins\n"
                             f"  {PLAYER_NAMES[1]}: {self.wins[1]} wins"))
            return

        self._next_turn()

    def _next_turn(self):
        self.current = 1 - self.current
        self._highlight_current()
        self.turn_label.config(text=f"{PLAYER_NAMES[self.current]}'s Turn")
        self.roll_btn.config(state="normal")

    # ── Drawing ───────────────────────────────────────────────────────────────

    def _draw_board(self):
        self.canvas.delete("all")
        num = 100
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                # Calculate cell number (bottom-left = 1, serpentine)
                if row % 2 == 0:
                    cell = row * BOARD_SIZE + col + 1
                else:
                    cell = row * BOARD_SIZE + (BOARD_SIZE - col)

                x1 = BOARD_OFFSET_X + col * CELL_SIZE
                y1 = BOARD_OFFSET_Y + (BOARD_SIZE - 1 - row) * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                color = BOARD_LIGHT if (row + col) % 2 == 0 else BOARD_DARK
                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=color, outline="#0D1B2A", width=1)
                # Cell number
                self.canvas.create_text(x1 + 5, y1 + 5, text=str(cell),
                                        anchor="nw", font=("Courier", 7),
                                        fill="#4CC9F0")

    def _draw_snakes_ladders(self):
        # Draw ladders
        for start, end in LADDERS.items():
            x1, y1 = cell_center(start)
            x2, y2 = cell_center(end)
            # Rails
            dx = (y2 - y1) / math.hypot(x2 - x1, y2 - y1) * 6
            dy = -(x2 - x1) / math.hypot(x2 - x1, y2 - y1) * 6
            self.canvas.create_line(x1 - dx, y1 - dy, x2 - dx, y2 - dy,
                                    fill=LADDER_COLOR, width=3)
            self.canvas.create_line(x1 + dx, y1 + dy, x2 + dx, y2 + dy,
                                    fill=LADDER_COLOR, width=3)
            # Rungs
            steps = 5
            for i in range(1, steps):
                rx = x1 + (x2 - x1) * i / steps
                ry = y1 + (y2 - y1) * i / steps
                self.canvas.create_line(rx - dx * 1.2, ry - dy * 1.2,
                                        rx + dx * 1.2, ry + dy * 1.2,
                                        fill=LADDER_COLOR, width=2)
            # Icons
            self.canvas.create_text(x1, y1, text="🪜", font=("", 13))
            self.canvas.create_text(x2, y2, text="⬆", font=("", 10), fill=LADDER_COLOR)

        # Draw snakes (bezier-ish with line segments)
        for start, end in SNAKES.items():
            x1, y1 = cell_center(start)
            x2, y2 = cell_center(end)
            # Draw a wavy line using multiple segments
            pts = []
            segs = 12
            cx, cy = (x1 + x2) / 2 + 30, (y1 + y2) / 2
            for i in range(segs + 1):
                t  = i / segs
                bx = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t ** 2 * x2
                by = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t ** 2 * y2
                pts.extend([bx, by])
            self.canvas.create_line(*pts, fill=SNAKE_COLOR, width=4,
                                    smooth=True, capstyle="round")
            self.canvas.create_text(x1, y1, text="🐍", font=("", 14))
            self.canvas.create_text(x2, y2, text="▼", font=("", 10), fill=SNAKE_COLOR)

    def _draw_players(self):
        self.canvas.delete("player")
        for i, pos in enumerate(self.positions):
            if pos == 0:
                continue
            cx, cy = cell_center(pos)
            offset = (-12 if i == 0 else 12)
            r = 11
            self.canvas.create_oval(cx + offset - r, cy - r,
                                    cx + offset + r, cy + r,
                                    fill=PLAYER_COLORS[i], outline="white",
                                    width=2, tags="player")
            self.canvas.create_text(cx + offset, cy,
                                    text=PLAYER_ICONS[i],
                                    font=("", 10, "bold"),
                                    fill="white", tags="player")

    def _draw_dice(self, value: int):
        c = self.dice_canvas
        c.delete("all")
        c.create_rectangle(4, 4, 76, 76, fill=DICE_BG, outline=ACCENT, width=2)
        dot_positions = {
            1: [(40, 40)],
            2: [(22, 22), (58, 58)],
            3: [(22, 22), (40, 40), (58, 58)],
            4: [(22, 22), (58, 22), (22, 58), (58, 58)],
            5: [(22, 22), (58, 22), (40, 40), (22, 58), (58, 58)],
            6: [(22, 20), (58, 20), (22, 40), (58, 40), (22, 60), (58, 60)],
        }
        if value == 0:
            c.create_text(40, 40, text="?", font=("Courier", 28, "bold"), fill=ACCENT)
            return
        for dx, dy in dot_positions[value]:
            c.create_oval(dx - 7, dy - 7, dx + 7, dy + 7, fill=ACCENT, outline="")

    def _highlight_current(self):
        for i, f in enumerate(self.player_frames):
            border = "white" if i == self.current else PLAYER_COLORS[i]
            f.config(highlightthickness=3 if i == self.current else 0,
                     highlightbackground=border)

    def _update_pos_labels(self):
        for i in range(2):
            self.pos_labels[i].config(text=f"Position: {self.positions[i]}")

    def _update_score_labels(self):
        for i in range(2):
            self.score_labels[i].config(text=f"Wins: {self.wins[i]}")

    # ── Log ───────────────────────────────────────────────────────────────────

    def _log(self, msg: str):
        self.log_box.config(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def _clear_log(self):
        self.log_box.config(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.config(state="disabled")


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = SnakeLadderApp()
    app.mainloop()
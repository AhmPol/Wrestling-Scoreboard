import tkinter as tk
from tkinter import messagebox
import time
from screeninfo import get_monitors

class WrestlingScoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wrestling Scoring App")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        self.root.configure(bg="black")
        self.reset_match()
        self.show_intro_screen()  
    
    def show_intro_screen(self):

        self.left_frame = tk.Frame(self.root, bg="red")
        self.left_frame.place(x=0, y=0, width=450, height=600)
        self.right_frame = tk.Frame(self.root, bg="blue")
        self.right_frame.place(x=450, y=0, width=450, height=600)

        tk.Label(self.left_frame, text="Wrestler 1 Name", font=("Arial", 24, "bold"), bg="red", fg="white").pack(pady=50)
        self.name1_entry = tk.Entry(self.left_frame, font=("Arial", 24), justify="center")
        self.name1_entry.pack(pady=10)

        tk.Label(self.right_frame, text="Wrestler 2 Name", font=("Arial", 24, "bold"), bg="blue", fg="white").pack(pady=50)
        self.name2_entry = tk.Entry(self.right_frame, font=("Arial", 24), justify="center")
        self.name2_entry.pack(pady=10)

        # Bout Number input
        tk.Label(self.root, text="Bout Number", font=("Arial", 20, "bold"), bg="black", fg="white").place(x=360, y=300)
        self.bout_entry = tk.Entry(self.root, font=("Arial", 20), justify="center")
        self.bout_entry.place(x=375, y=340, width=150)

        tk.Button(self.root, text="Start Match", font=("Arial", 20, "bold"), command=self.start_match, bg="gray", fg="white").place(x=375, y=500, width=150, height=60)

    def start_match(self):
        self.wrestler1 = self.name1_entry.get() or "Wrestler 1"
        self.wrestler2 = self.name2_entry.get() or "Wrestler 2"
        self.bout_number = self.bout_entry.get() or "N/A"
        self.reset_match()
        self.show_match_screen()
        self.show_scoreboard_screen()

    def show_match_screen(self):
        self.clear_window()
        self.create_widgets()
        self.bind_keys()

    def reset_match(self):
        self.score1 = 0
        self.score2 = 0
        self.history = []
        self.timer_state = "Period 1"
        self.time_left = 120
        self.running = False
        self.start_time = None
        self.timer_clicked = False

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_widgets(self):
        self.left_frame = tk.Frame(self.root, bg="red")
        self.left_frame.place(x=0, y=0, width=450, height=200)
        self.right_frame = tk.Frame(self.root, bg="blue")
        self.right_frame.place(x=450, y=0, width=450, height=200)

        self.name1_label = tk.Label(self.left_frame, text=self.wrestler1, font=("Arial", 32, "bold"), bg="red", fg="white")
        self.name1_label.place(x=50, y=20, width=350)

        self.score1_label = tk.Label(self.left_frame, text="0", font=("Arial", 60, "bold"), bg="red", fg="white")
        self.score1_label.place(x=190, y=80)

        self.name2_label = tk.Label(self.right_frame, text=self.wrestler2, font=("Arial", 32, "bold"), bg="blue", fg="white")
        self.name2_label.place(x=50, y=20, width=350)

        self.score2_label = tk.Label(self.right_frame, text="0", font=("Arial", 60, "bold"), bg="blue", fg="white")
        self.score2_label.place(x=190, y=80)

        self.time_label = tk.Label(self.root, text="2:00", font=("Arial", 36), bg="black", fg="white")
        self.time_label.place(x=400, y=220)

        self.period_label = tk.Label(self.root, text="Period 1", font=("Arial", 24), bg="black", fg="white")
        self.period_label.place(x=390, y=270)

        self.start_stop_button = tk.Button(self.root, text="START/STOP", command=self.toggle_timer, bg="gray", fg="white", font=("Arial", 14, "bold"))
        self.start_stop_button.place(x=385, y=310, width=130, height=40)

        self.create_score_buttons()
        self.create_result_buttons()

    def create_score_buttons(self):
        btn_cfg = {'bg': 'white', 'fg': 'black', 'font': ("Arial", 14, "bold")}
        for i, (points, x, side) in enumerate([  
            (1, 40, 1), (2, 120, 1), (4, 200, 1),  
            (1, 630, 2), (2, 710, 2), (4, 790, 2), 
        ]):
            label = f"+{points}"
            tk.Button(self.root, text=label, command=lambda p=points, s=side: self.update_score(p, s),
                      **btn_cfg).place(x=x, y=360, width=70, height=70)

    def create_result_buttons(self):
        tk.Button(self.root, text="PIN", command=lambda: self.end_match("PIN", 1),
                  bg="red", fg="white", font=("Arial", 14, "bold")).place(x=50, y=450, width=100, height=60)
        tk.Button(self.root, text="TECH", command=lambda: self.end_match("TECH", 1),
                  bg="red", fg="white", font=("Arial", 14, "bold")).place(x=160, y=450, width=100, height=60)
        tk.Button(self.root, text="PIN", command=lambda: self.end_match("PIN", 2),
                  bg="blue", fg="white", font=("Arial", 14, "bold")).place(x=640, y=450, width=100, height=60)
        tk.Button(self.root, text="TECH", command=lambda: self.end_match("TECH", 2),
                  bg="blue", fg="white", font=("Arial", 14, "bold")).place(x=750, y=450, width=100, height=60)

        tk.Button(self.root, text="DECISION", command=self.handle_decision_result,
                  bg="gray", fg="white", font=("Arial", 14, "bold")).place(x=400, y=440, width=100, height=40)
        tk.Button(self.root, text="RESET", command=self.show_intro_screen,
                  bg="gray", fg="white", font=("Arial", 14, "bold")).place(x=400, y=500, width=100, height=40)

    def bind_keys(self):
        self.root.bind("<space>", lambda e: self.toggle_timer() if self.timer_clicked else None)
        self.root.bind("<BackSpace>", lambda e: self.undo_last())

    def toggle_timer(self):
        self.running = not self.running
        self.timer_clicked = True
        if self.running:
            if self.start_time is None:
                self.start_time = time.time()
            self.update_timer()

    def update_timer(self):
        if self.running and self.time_left > 0:
            self.time_left -= 1
            mins, secs = divmod(self.time_left, 60)
            self.time_label.config(text=f"{mins}:{secs:02d}")
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.running = False
            self.advance_timer_state()

    def advance_timer_state(self):
        if self.timer_state == "Period 1":
            self.timer_state = "Break"
            self.time_left = 30
        elif self.timer_state == "Break":
            self.timer_state = "Period 2"
            self.time_left = 120
        elif self.timer_state == "Period 2":
            self.timer_state = "Match Over"
        self.period_label.config(text=self.timer_state)
        self.time_label.config(text=f"{self.time_left // 60}:{self.time_left % 60:02d}")

    def update_score(self, points, side):
        timestamp = self.time_left
        if side == 1:
            self.score1 += points
            self.score1_label.config(text=str(self.score1))
        elif side == 2:
            self.score2 += points
            self.score2_label.config(text=str(self.score2))
        self.history.append((points, side, timestamp))

    def undo_last(self):
        if self.history:
            points, side, _ = self.history.pop()
            if side == 1:
                self.score1 = max(0, self.score1 - points)
                self.score1_label.config(text=str(self.score1))
            elif side == 2:
                self.score2 = max(0, self.score2 - points)
                self.score2_label.config(text=str(self.score2))

    def handle_decision_result(self):
        if self.running:
            messagebox.showwarning("Pause Timer", "Pause the timer before declaring a decision.")
            return

        if self.score1 > self.score2:
            winner = 1
        elif self.score2 > self.score1:
            winner = 2
        else:
            # Compare valuable points
            valuable1 = sum(p for p, s, _ in self.history if s == 1 and p == 4)  # Total 4-point score for Wrestler 1
            valuable2 = sum(p for p, s, _ in self.history if s == 2 and p == 4)  # Total 4-point score for Wrestler 2
            
            if valuable1 > valuable2:
                winner = 1
            elif valuable2 > valuable1:
                winner = 2
            else:
                # If valuable points are equal, determine who scored last
                last = next(reversed(self.history), None)
                winner = last[1] if last else 1  # Default to wrestler 1 if no last score

        self.end_match("DECISION", winner)

    def end_match(self, method, winner):
        name1 = self.wrestler1
        name2 = self.wrestler2

        tk.Label(self.root, text=f"Bout {self.bout_number}: {name1 if winner == 1 else name2} WINS by {method}",
                 font=("Arial", 28, "bold"), fg="white", bg="black").pack(pady=10)

        result_frame = tk.Frame(self.root, bg="black")
        result_frame.pack(fill="both", expand=True)

        left = tk.Frame(result_frame, bg="red")
        right = tk.Frame(result_frame, bg="blue")
        left.pack(side="left", fill="both", expand=True)
        right.pack(side="right", fill="both", expand=True)

        tk.Label(left, text=name1, font=("Arial", 24, "bold"), bg="red", fg="white").pack(pady=10)
        tk.Label(left, text=str(self.score1), font=("Arial", 48, "bold"), bg="red", fg="white").pack()

        tk.Label(right, text=name2, font=("Arial", 24, "bold"), bg="blue", fg="white").pack(pady=10)
        tk.Label(right, text=str(self.score2), font=("Arial", 48, "bold"), bg="blue", fg="white").pack()

        tk.Label(left, text="\n".join([f"{p} Points - {t//60}:{t%60:02d}" for p, s, t in self.history if s == 1]) or "None",
                 font=("Arial", 14), bg="red", fg="white").pack(pady=30)
        tk.Label(right, text="\n".join([f"{p} Points - {t//60}:{t%60:02d}" for p, s, t in self.history if s == 2]) or "None",
                 font=("Arial", 14), bg="blue", fg="white").pack(pady=30)

        tk.Button(self.root, text="OK", command=self.show_intro_screen, bg="gray", fg="white",
                  font=("Arial", 16)).pack(pady=10)

    def show_scoreboard_screen(self):
        # If scoreboard exists, update it instead of recreating
        if hasattr(self, 'scoreboard') and self.scoreboard.winfo_exists():
            self.sb_bout.config(text=f"BOUT {self.bout_number}")
            self.sb_name1.config(text=self.wrestler1)
            self.sb_entry1.delete(0, tk.END)
            self.sb_entry1.insert(0, "0")
            self.sb_name2.config(text=self.wrestler2)
            self.sb_entry2.delete(0, tk.END)
            self.sb_entry2.insert(0, "0")
            self.scoreboard_window.update()
            return

        # Create new scoreboard window
        self.scoreboard = tk.Toplevel(self.root)
        self.scoreboard.title("Live Scoreboard")
        self.scoreboard.configure(bg="black")

        # Define font sizes relative to the window size (adjusting scaling factor to make text bigger)
        window_width = self.scoreboard.winfo_width()
        window_height = self.scoreboard.winfo_height()

        font_size_bout = int(60)  # Larger font size
        font_size_timer = int(110)  # Larger font size for timer
        font_size_name = int(60)  # Larger font size for names
        font_size_score = int(180)  # Larger font size for scores

        # Bout number
        self.sb_bout = tk.Label(self.scoreboard, text=f"BOUT {self.bout_number}", 
                                font=("Arial", font_size_bout, "bold"), bg="black", fg="white")
        self.sb_bout.pack(pady=10)

        # Create red and blue panels
        frame = tk.Frame(self.scoreboard, bg="black")
        frame.pack(fill="both", expand=True)

        self.sb_timer = tk.Label(self.scoreboard, text="2:00", font=("Arial", font_size_timer, "bold"), bg="black", fg="white")
        self.sb_timer.pack(pady=5)

        left = tk.Frame(frame, bg="red", width=400)
        right = tk.Frame(frame, bg="blue", width=400)
        left.pack(side="left", fill="both", expand=True)
        right.pack(side="right", fill="both", expand=True)

        # Red (Left Side)
        self.sb_name1 = tk.Label(left, text=self.wrestler1, font=("Arial", font_size_name, "bold"), bg="red", fg="white")
        self.sb_name1.pack(pady=10)

        self.sb_score1 = tk.Label(left, text="0", font=("Arial", font_size_score, "bold"), bg="red", fg="white", width=4)
        self.sb_score1.pack(pady=20)

        # Blue (Right Side)
        self.sb_name2 = tk.Label(right, text=self.wrestler2, font=("Arial", font_size_name, "bold"), bg="blue", fg="white")
        self.sb_name2.pack(pady=10)

        self.sb_score2 = tk.Label(right, text="0", font=("Arial", font_size_score, "bold"), bg="blue", fg="white", width=4)
        self.sb_score2.pack(pady=20)

        # Optional: Esc to close
        self.scoreboard.bind("<Escape>", lambda e: self.scoreboard.destroy())

            # Functionality for maximizing to fullscreen on the extended screen
        def maximize_window(event=None):
            # Get the extended screen (second monitor)
            monitors = get_monitors()
            if len(monitors) > 1:
                # Assuming the second screen is the extended one
                second_monitor = monitors[1]
                screen_width = second_monitor.width * 3
                screen_height = second_monitor.height * 3
                screen_x = second_monitor.x
                screen_y = second_monitor.y
            else:
                # Fallback to primary monitor if no extended screen is found
                screen_width = self.scoreboard.winfo_screenwidth()
                screen_height = self.scoreboard.winfo_screenheight()
                screen_x = 0
                screen_y = 0

            # Set the window size and position to match the second monitor
            self.scoreboard.geometry(f"{screen_width}x{screen_height}+{screen_x}+{screen_y}")

        # Bind the 'Q' key to maximize the window
        self.scoreboard.bind('<q>', maximize_window)

        # Update the scoreboard every second
        self.update_scoreboard()

    def update_scoreboard(self):
        if hasattr(self, 'sb_score1') and hasattr(self, 'sb_score2'):
            # Update score
            self.sb_score1.config(text=str(self.score1))
            self.sb_score2.config(text=str(self.score2))
            
            # Update timer
            mins, secs = divmod(self.time_left, 60)
            self.sb_timer.config(text=f"{mins}:{secs:02d}")

            # Refresh every 1000ms (1 second)
            self.scoreboard.after(1000, self.update_scoreboard)

# Run the app
root = tk.Tk()
app = WrestlingScoringApp(root)
root.mainloop()

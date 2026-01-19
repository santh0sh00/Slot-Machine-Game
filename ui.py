# ui.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from main import get_slot_machine_spin, check_winnings, symbol_count, symbol_value, ROWS, COLS, MAX_LINES, MIN_BET, MAX_BET


class SlotMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 Cute Slot Machine Game 🎰")
        self.root.geometry("600x500")
        self.root.config(bg="#222831")

        # Variables
        self.balance = 0
        self.bet = tk.IntVaqr(value=MIN_BET)
        self.lines = tk.IntVar(value=1)

        # Title
        title = tk.Label(root, text="🎰 Slot Machine 🎰", font=("Comic Sans MS", 26, "bold"),
                         fg="#FFD700", bg="#222831")
        title.pack(pady=10)

        # Balance Frame
        balance_frame = tk.Frame(root, bg="#393E46")
        balance_frame.pack(pady=10)
        tk.Label(balance_frame, text="💰 Balance: $", font=("Arial", 14),
                 fg="white", bg="#393E46").pack(side="left")
        self.balance_label = tk.Label(balance_frame, text=str(self.balance), font=("Arial", 14, "bold"),
                                      fg="#00FFAB", bg="#393E46")
        self.balance_label.pack(side="left", padx=5)
        tk.Button(balance_frame, text="Deposit", font=("Arial", 12),
                  command=self.deposit, bg="#FFD369", fg="black").pack(side="left", padx=10)

        # Settings Frame
        settings_frame = tk.Frame(root, bg="#393E46")
        settings_frame.pack(pady=10)
        tk.Label(settings_frame, text="Bet per line: $", font=("Arial", 12),
                 bg="#393E46", fg="white").grid(row=0, column=0, padx=5)
        tk.Entry(settings_frame, textvariable=self.bet, width=10).grid(row=0, column=1)

        tk.Label(settings_frame, text="Lines (1–3):", font=("Arial", 12),
                 bg="#393E46", fg="white").grid(row=0, column=2, padx=5)
        tk.Entry(settings_frame, textvariable=self.lines, width=10).grid(row=0, column=3)

        # Slot Area
        self.slot_frame = tk.Frame(root, bg="#222831")
        self.slot_frame.pack(pady=30)

        self.slots_labels = []
        for r in range(ROWS):
            row_labels = []
            for c in range(COLS):
                lbl = tk.Label(self.slot_frame, text="❔", font=("Arial", 32, "bold"),
                               width=3, bg="#393E46", fg="#FFD700", relief="ridge", borderwidth=3)
                lbl.grid(row=r, column=c, padx=10, pady=5)
                row_labels.append(lbl)
            self.slots_labels.append(row_labels)

        # Play Button
        tk.Button(root, text="SPIN 🎲", font=("Arial", 18, "bold"),
                  command=self.play, bg="#00ADB5", fg="white", width=12).pack(pady=15)

        # Result Label
        self.result_label = tk.Label(root, text="", font=("Comic Sans MS", 14, "bold"),
                                     fg="white", bg="#222831")
        self.result_label.pack(pady=10)

    # --- Game Logic Wrappers ---
    def deposit(self):
        amount = simpledialog.askinteger("Deposit", "Enter deposit amount ($):", minvalue=1)
        if amount:
            self.balance += amount
            self.balance_label.config(text=str(self.balance))
            messagebox.showinfo("Deposit Successful", f"Deposited ${amount} successfully!")

    def play(self):
        bet = self.bet.get()
        lines = self.lines.get()

        if bet < MIN_BET or bet > MAX_BET:
            messagebox.showerror("Error", f"Bet must be between ${MIN_BET} and ${MAX_BET}.")
            return
        if lines < 1 or lines > MAX_LINES:
            messagebox.showerror("Error", f"Lines must be between 1 and {MAX_LINES}.")
            return

        total_bet = bet * lines
        if total_bet > self.balance:
            messagebox.showerror("Insufficient Balance", "Not enough balance to play!")
            return

        self.balance -= total_bet
        self.balance_label.config(text=str(self.balance))

        # Spin and display
        slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
        for r in range(ROWS):
            for c in range(COLS):
                self.slots_labels[r][c].config(text=slots[c][r])

        winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
        self.balance += winnings
        self.balance_label.config(text=str(self.balance))

        if winnings > 0:
            msg = f"🎉 You won ${winnings} on lines {', '.join(map(str, winning_lines))}!"
            color = "#00FFAB"
        else:
            msg = "😢 No win this time, try again!"
            color = "#FF6363"
        self.result_label.config(text=msg, fg=color)


# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SlotMachineApp(root)
    root.mainloop()

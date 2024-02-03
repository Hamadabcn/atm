import tkinter as tk
from tkinter import simpledialog, messagebox

class CashMachine:
    def __init__(self):
        self.balance = 0
        self.transaction_history = []

    def check_balance(self):
        return f"Your current balance: €{self.balance}"

    def withdraw_money(self, amount):
        if self.balance < amount:
            result = "Insufficient funds. Unable to withdraw."
        else:
            self.balance -= amount
            result = f"Withdrawal: -€{amount}. New balance: €{self.balance}"
            self.transaction_history.append(result)
        return result

    def deposit_money(self, amount):
        self.balance += amount
        result = f"Deposit: +€{amount}. New balance: €{self.balance}"
        self.transaction_history.append(result)
        return result

class CashMachineGUI:
    def __init__(self, root):
        self.cash_machine = CashMachine()

        self.root = root
        self.root.title("Cash Machine GUI")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="CASH MACHINE", font=("Helvetica", 22, "bold"), bg="#4CAF50", fg="white")
        title_label.pack(pady=10)

        # Set the initial balance label
        self.balance_label = tk.Label(self.root, text="", font=("Helvetica", 18))
        self.balance_label.pack(pady=10)

        menu_frame = tk.Frame(self.root, bg="#f0f0f0")
        menu_frame.pack(pady=20)

        balance_button = tk.Button(menu_frame, text="Check Balance", command=lambda: self.update_label(self.balance_label, self.cash_machine.check_balance()), font=("Helvetica", 14))
        balance_button.grid(row=0, column=0, padx=10)

        withdraw_button = tk.Button(menu_frame, text="Withdraw Money", command=self.withdraw_money, font=("Helvetica", 14))
        withdraw_button.grid(row=0, column=1, padx=10)

        deposit_button = tk.Button(menu_frame, text="Deposit Money", command=self.deposit_money, font=("Helvetica", 14))
        deposit_button.grid(row=0, column=2, padx=10)

        history_button = tk.Button(menu_frame, text="Show History", command=self.show_history, font=("Helvetica", 14))
        history_button.grid(row=0, column=3, padx=10)

        quit_button = tk.Button(self.root, text="Quit", command=self.quit_program, bg="#d32f2f", fg="white", font=("Helvetica", 14))
        quit_button.pack()

        # Entry widgets for direct input
        self.amount_entry = tk.Entry(menu_frame, font=("Helvetica", 14), width=10)
        self.amount_entry.grid(row=1, column=1, pady=10)
        self.amount_entry.insert(0, "0.00")  # Default value

        # Labels for Entry widgets
        amount_label = tk.Label(menu_frame, text="Amount (€):", font=("Helvetica", 14), bg="#f0f0f0")
        amount_label.grid(row=1, column=0)

        # Frame for displaying transaction history
        self.history_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.history_frame.pack(pady=20)

        # Text widget to display history
        self.history_text = tk.Text(self.history_frame, height=10, width=60, wrap=tk.WORD, font=("Helvetica", 12))
        self.history_text.pack()

    def update_label(self, label, text):
        label.config(text=text)

    def withdraw_money(self):
        try:
            amount = float(self.amount_entry.get())
            result = self.cash_machine.withdraw_money(amount)
            self.update_label(tk.Label(self.root, text=result, font=("Helvetica", 12)), result)
            self.update_label(self.balance_label, self.cash_machine.check_balance())  # Update balance label
        except ValueError:
            self.update_label(tk.Label(self.root, text="Invalid input. Please enter a valid amount.", font=("Helvetica", 12)), "Invalid input. Please enter a valid amount.")

    def deposit_money(self):
        try:
            amount = float(self.amount_entry.get())
            result = self.cash_machine.deposit_money(amount)
            self.update_label(tk.Label(self.root, text=result, font=("Helvetica", 12)), result)
            self.update_label(self.balance_label, self.cash_machine.check_balance())  # Update balance label
        except ValueError:
            self.update_label(tk.Label(self.root, text="Invalid input. Please enter a valid amount.", font=("Helvetica", 12)), "Invalid input. Please enter a valid amount.")

    def show_history(self):
        self.history_text.delete(1.0, tk.END)  # Clear previous history
        history_text = "\n".join(self.cash_machine.transaction_history)
        self.history_text.insert(tk.END, history_text)

    def quit_program(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CashMachineGUI(root)
    root.mainloop()

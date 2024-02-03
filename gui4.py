import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime  # Import the datetime module

class CashMachine:
    def __init__(self):
        self.balance = 0
        self.transaction_history = []

    def check_balance(self):
        return f"Your current balance: €{self.balance}"

    def withdraw_money(self, amount):
        transaction_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")  # European date format
        if self.balance < amount:
            result = "Insufficient funds. Unable to withdraw."
        else:
            self.balance -= amount
            result = f"Withdrawal: -€{amount}. New balance: €{self.balance}. Date: {transaction_time}"
            self.transaction_history.append(result)
        return result

    def deposit_money(self, amount):
        transaction_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")  # European date format
        self.balance += amount
        result = f"Deposit: +€{amount}. New balance: €{self.balance}. Date: {transaction_time}"
        self.transaction_history.append(result)
        return result

class CashMachineGUI:
    def __init__(self, root):
        self.cash_machine = CashMachine()

        self.root = root
        self.root.title("Cash Machine GUI")
        self.root.geometry("600x700")
        self.root.configure(bg="#263238")  # Dark background color

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="CASH MACHINE", font=("Helvetica", 22, "bold"), bg="#37474F", fg="white")
        title_label.pack(pady=10)

        # Set the initial balance label
        self.balance_label = tk.Label(self.root, text=self.cash_machine.check_balance(), font=("Helvetica", 18), bg="#263238", fg="white")
        self.balance_label.pack(pady=10)

        menu_frame = tk.Frame(self.root, bg="#263238")  # Dark background color
        menu_frame.pack(pady=20)

        withdraw_button = tk.Button(menu_frame, text="Withdraw Money", command=self.withdraw_money, font=("Helvetica", 14), bg="#2979FF", fg="white")  # Dark blue button
        withdraw_button.grid(row=0, column=0, padx=10)

        deposit_button = tk.Button(menu_frame, text="Deposit Money", command=self.deposit_money, font=("Helvetica", 14), bg="#2979FF", fg="white")  # Dark blue button
        deposit_button.grid(row=0, column=1, padx=10)

        history_button = tk.Button(menu_frame, text="Show History", command=self.show_history, font=("Helvetica", 14), bg="#2979FF", fg="white")  # Dark blue button
        history_button.grid(row=0, column=2, padx=10)

        quit_button = tk.Button(self.root, text="Quit", command=self.quit_program, bg="#d32f2f", fg="white", font=("Helvetica", 14))
        quit_button.pack()

        # Entry widgets for direct input
        self.amount_entry = tk.Entry(menu_frame, font=("Helvetica", 14), width=20, justify="left", insertwidth=4)
        self.amount_entry.grid(row=1, column=0, pady=10)
        self.amount_entry.insert(0, "Enter amount")  # Default placeholder text
        self.amount_entry.bind("<FocusIn>", self.clear_default_text)  # Bind event handler for focus in

        # Frame for displaying transaction history
        self.history_frame = tk.Frame(self.root, bg="#263238")  # Dark background color
        self.history_frame.pack(pady=20)

        # Text widget to display history (increased height to 20)
        self.history_text = tk.Text(self.history_frame, height=20, width=60, wrap=tk.WORD, font=("Helvetica", 12), bg="#455A64", fg="white")  # Dark text area
        self.history_text.pack()

    def withdraw_money(self):
        try:
            amount = float(self.amount_entry.get())
            result = self.cash_machine.withdraw_money(amount)
            self.update_text(result)
            self.update_label(self.balance_label, self.cash_machine.check_balance())  # Update balance label
        except ValueError:
            error_message = "Invalid input. Please enter a valid amount."
            self.update_text(error_message)

    def deposit_money(self):
        try:
            amount = float(self.amount_entry.get())
            result = self.cash_machine.deposit_money(amount)
            self.update_text(result)
            self.update_label(self.balance_label, self.cash_machine.check_balance())  # Update balance label
        except ValueError:
            error_message = "Invalid input. Please enter a valid amount."
            self.update_text(error_message)

    def show_history(self):
        self.history_text.delete(1.0, tk.END)  # Clear previous history
        history_text = "\n".join(self.cash_machine.transaction_history)
        self.history_text.insert(tk.END, history_text)

    def quit_program(self):
        self.root.destroy()

    def clear_default_text(self, event):
        if self.amount_entry.get() == "Enter amount":
            self.amount_entry.delete(0, tk.END)
        self.amount_entry.icursor(0)  # Move the cursor to the beginning

    def update_label(self, label, text):
        label.config(text=text)

    def update_text(self, text):
        self.history_text.insert(tk.END, text + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = CashMachineGUI(root)
    root.mainloop()

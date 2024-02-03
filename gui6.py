import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime
import locale

# Class representing the Cash Machine functionality
class CashMachine:
    def __init__(self):
        # Initialize balance, transaction history, and hardcoded PIN
        self.balance = 0
        self.transaction_history = []
        self.pin = "1234"  # Hardcoded PIN to "1234"

    def check_balance(self):
        return f"Your current balance: {self.format_currency(self.balance)}"

    def withdraw_money(self, amount):
        # Get the current timestamp for the transaction
        transaction_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        # Check if the PIN is set and there are sufficient funds
        if self.pin and self.balance >= amount:
            self.balance -= amount
            # Record the withdrawal transaction in the history
            result = f"Withdrawal: -{self.format_currency(amount)}. New balance: {self.format_currency(self.balance)}. Date: {transaction_time}"
            self.transaction_history.append(result)
            return result
        else:
            return "Insufficient funds. Unable to withdraw."

    def deposit_money(self, amount):
        # Get the current timestamp for the transaction
        transaction_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        # Check if the PIN is set
        if self.pin:
            self.balance += amount
            # Record the deposit transaction in the history
            result = f"Deposit: +{self.format_currency(amount)}. New balance: {self.format_currency(self.balance)}. Date: {transaction_time}"
            self.transaction_history.append(result)
            return result
        else:
            return "Unable to deposit."

    def format_currency(self, amount):
        return locale.currency(amount, grouping=True)

# Class holding constants for GUI styling
class GUIConstants:
    BACKGROUND_COLOR = "#263238"
    BUTTON_COLOR = "#2979FF"
    ERROR_COLOR = "#d32f2f"
    TEXT_AREA_COLOR = "#455A64"
    TEXT_COLOR = "white"
    FONT_STYLE = ("Helvetica", 14)

# Class representing the Cash Machine GUI
class CashMachineGUI:
    def __init__(self, root):
        # Initialize CashMachine instance and prompt for PIN
        self.cash_machine = CashMachine()
        self.verify_pin()
        self.root = root
        self.root.title("ATM GUI")
        self.root.geometry("600x700")
        self.root.configure(bg=GUIConstants.BACKGROUND_COLOR)

        # Create GUI widgets
        self.create_widgets()

    def verify_pin(self):
        # Loop until a correct PIN is entered
        while True:
            pin = simpledialog.askstring("PIN", "Enter your 4-digit PIN:")
            if pin == self.cash_machine.pin:
                break
            else:
                messagebox.showerror("Error", "Invalid PIN. Please try again.")

    def create_widgets(self):
        # Create and pack GUI elements
        title_label = tk.Label(self.root, text="ATM", font=("Helvetica", 28, "bold"), bg=GUIConstants.BUTTON_COLOR, fg=GUIConstants.TEXT_COLOR)
        title_label.pack(pady=10)

        self.balance_label = tk.Label(self.root, text=self.cash_machine.check_balance(), font=("Helvetica", 18), bg=GUIConstants.BACKGROUND_COLOR, fg=GUIConstants.TEXT_COLOR)
        self.balance_label.pack(pady=10)

        menu_frame = tk.Frame(self.root, bg=GUIConstants.BACKGROUND_COLOR)
        menu_frame.pack(pady=20)

        withdraw_button = tk.Button(menu_frame, text="Withdraw Money", command=self.withdraw_money, font=GUIConstants.FONT_STYLE, bg=GUIConstants.BUTTON_COLOR, fg=GUIConstants.TEXT_COLOR)
        withdraw_button.grid(row=0, column=0, padx=10)

        deposit_button = tk.Button(menu_frame, text="Deposit Money", command=self.deposit_money, font=GUIConstants.FONT_STYLE, bg=GUIConstants.BUTTON_COLOR, fg=GUIConstants.TEXT_COLOR)
        deposit_button.grid(row=0, column=1, padx=10)

        history_button = tk.Button(menu_frame, text="Show History", command=self.show_history, font=GUIConstants.FONT_STYLE, bg=GUIConstants.BUTTON_COLOR, fg=GUIConstants.TEXT_COLOR)
        history_button.grid(row=0, column=2, padx=10)

        quit_button = tk.Button(self.root, text="Quit", command=self.quit_program, bg=GUIConstants.ERROR_COLOR, fg=GUIConstants.TEXT_COLOR, font=GUIConstants.FONT_STYLE)
        quit_button.pack()

        self.amount_entry = tk.Entry(menu_frame, font=GUIConstants.FONT_STYLE, width=20, justify="left", insertwidth=4)
        self.amount_entry.grid(row=1, column=0, pady=10)
        self.amount_entry.insert(0, "Enter amount")
        self.amount_entry.bind("<FocusIn>", self.clear_default_text)

        self.history_frame = tk.Frame(self.root, bg=GUIConstants.BACKGROUND_COLOR)
        self.history_frame.pack(pady=20)

        self.history_text = tk.Text(self.history_frame, height=20, width=60, wrap=tk.WORD, font=("Helvetica", 12), bg=GUIConstants.TEXT_AREA_COLOR, fg=GUIConstants.TEXT_COLOR)
        self.history_text.pack()

    def withdraw_money(self):
        try:
            amount = float(self.amount_entry.get())
            result = self.cash_machine.withdraw_money(amount)
            self.update_text(result)
            self.update_label(self.balance_label, self.cash_machine.check_balance())
        except ValueError:
            error_message = "Invalid input. Please enter a valid amount."
            self.update_text(error_message)

    def deposit_money(self):
        try:
            amount = float(self.amount_entry.get())
            result = self.cash_machine.deposit_money(amount)
            self.update_text(result)
            self.update_label(self.balance_label, self.cash_machine.check_balance())
        except ValueError:
            error_message = "Invalid input. Please enter a valid amount."
            self.update_text(error_message)

    def show_history(self):
        self.history_text.delete(1.0, tk.END)
        history_text = "\n".join(self.cash_machine.transaction_history)
        self.history_text.insert(tk.END, history_text)

    def quit_program(self):
        self.root.destroy()

    def clear_default_text(self, event):
        if self.amount_entry.get() == "Enter amount":
            self.amount_entry.delete(0, tk.END)
        self.amount_entry.icursor("end")  # Move the cursor to the end

    def update_label(self, label, text):
        label.config(text=text)

    def update_text(self, text):
        self.history_text.insert(tk.END, text + "\n")

# Entry point of the script
if __name__ == "__main__":
    # Set the locale to the user's default
    locale.setlocale(locale.LC_ALL, '')
    # Create the Tkinter root window
    root = tk.Tk()
    # Create an instance of the CashMachineGUI class
    app = CashMachineGUI(root)
    # Start the Tkinter event loop
    root.mainloop()

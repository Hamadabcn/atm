# latest version

import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime
import locale

class CashMachine:
    """Class representing the Cash Machine"""

    def __init__(self):
        """Initialize Cash Machine attributes"""
        self.balance = 0
        self.transaction_history = []
        self.pin = None  # Default PIN is None

    def check_balance(self):
        """Return a formatted string indicating the current balance"""
        return f"Your current balance: {self.format_currency(self.balance)}"

    def set_pin(self, pin):
        """
        Set the PIN if it's a 4-digit number.

        Args:
            pin (str): The PIN to set.

        Returns:
            bool: True if the PIN is set successfully, False otherwise.
        """
        if pin.isdigit() and len(pin) == 4:
            self.pin = pin
            return True
        else:
            return False

    def verify_pin(self, pin):
        """
        Verify if the entered PIN matches the stored PIN.

        Args:
            pin (str): The PIN to verify.

        Returns:
            bool: True if the PIN is verified successfully, False otherwise.
        """
        return self.pin == pin

    def withdraw_money(self, amount):
        """
        Withdraw money from the cash machine.

        Args:
            amount (float): The amount to be withdrawn.

        Returns:
            tuple: A tuple containing a transaction result message (str) and success status (bool).
        """
        transaction_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        if self.pin and amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                result = f"Withdrawal: -{self.format_currency(amount)}. New balance: {self.format_currency(self.balance)}. Date: {transaction_time}"
                self.transaction_history.append(result)
                return result, True
            else:
                return "Insufficient funds. Withdrawal amount exceeds the current balance.", False
        else:
            if amount <= 0:
                return "Invalid withdrawal amount. Amount must be greater than 0.", False
            elif not self.pin:
                return "Invalid operation. PIN not set.", False
            elif not self.verify_pin(self.pin):
                return "Invalid PIN. Please enter the correct PIN.", False

    def deposit_money(self, amount):
        """
        Deposit money into the cash machine.

        Args:
            amount (float): The amount to be deposited.

        Returns:
            tuple: A tuple containing a transaction result message (str) and success status (bool).
        """
        transaction_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        if self.pin and amount > 0:
            self.balance += amount
            result = f"Deposit: +{self.format_currency(amount)}. New balance: {self.format_currency(self.balance)}. Date: {transaction_time}"
            self.transaction_history.append(result)
            return result, True
        else:
            if amount <= 0:
                return "Invalid deposit amount. Amount must be greater than 0.", False
            elif not self.pin:
                return "Invalid operation. PIN not set.", False
            elif not self.verify_pin(self.pin):
                return "Invalid PIN. Please enter the correct PIN.", False

    def format_currency(self, amount):
        """
        Format the amount as currency using the locale module.

        Args:
            amount (float): The amount to be formatted.

        Returns:
            str: The formatted amount as currency.
        """
        return locale.currency(amount, grouping=True, symbol='€')

class TransactionHandler:
    """Class handling transactions"""

    def __init__(self, cash_machine):
        """Initialize TransactionHandler with a CashMachine instance"""
        self.cash_machine = cash_machine

    def perform_withdrawal(self, amount):
        """
        Perform a withdrawal transaction.

        Args:
            amount (float): The amount to be withdrawn.

        Returns:
            tuple: A tuple containing a transaction result message (str) and success status (bool).
        """
        try:
            result, success = self.cash_machine.withdraw_money(amount)
            return result, success
        except ValueError as e:
            if "Insufficient funds" in str(e):
                return "Insufficient funds. Withdrawal amount exceeds the current balance.", False
            else:
                return f"Error: {str(e)}", False

    def perform_deposit(self, amount):
        """
        Perform a deposit transaction.

        Args:
            amount (float): The amount to be deposited.

        Returns:
            tuple: A tuple containing a transaction result message (str) and success status (bool).
        """
        try:
            result, success = self.cash_machine.deposit_money(amount)
            return result, success
        except ValueError as e:
            return f"Error: {str(e)}", False

class GUIConstants:
    """Class containing constants for GUI styling"""
    BACKGROUND_COLOR = "#263238"
    BUTTON_COLOR = "#2979FF"
    SUCCESS_COLOR = "#4CAF50"
    FAILURE_COLOR = "#d32f2f"  # Red color for failure
    TEXT_AREA_COLOR = "#455A64"
    TEXT_COLOR = "white"
    FONT_STYLE = ("Helvetica", 14)

class CashMachineGUI:
    """Class representing the Cash Machine GUI"""

    def __init__(self, root, transaction_handler):
        """
        Initialize CashMachineGUI with a Tkinter root and a TransactionHandler instance.

        Args:
            root (tk.Tk): The Tkinter root.
            transaction_handler (TransactionHandler): The TransactionHandler instance.
        """
        self.transaction_handler = transaction_handler
        self.showing_history = False
        self.root = root
        self.verify_pin()
        self.root.title("ATM GUI")
        self.root.geometry("600x700")
        self.root.configure(bg=GUIConstants.BACKGROUND_COLOR)
        self.create_widgets()

    def verify_pin(self):
        """Prompt the user to set a 4-digit PIN and handle invalid inputs"""
        while True:
            pin = simpledialog.askstring("PIN", "Enter your 4-digit PIN:")
            if self.transaction_handler.cash_machine.set_pin(pin):
                messagebox.showinfo("PIN Set", "PIN successfully set!")
                break
            else:
                messagebox.showerror("Error", "Invalid PIN. Please enter a 4-digit PIN.")

    def create_widgets(self):
        """Create GUI widgets"""
        title_label = tk.Label(self.root, text="ATM", font=("Helvetica", 28, "bold"), bg=GUIConstants.BUTTON_COLOR, fg=GUIConstants.TEXT_COLOR)
        title_label.pack(pady=10)

        self.balance_label = tk.Label(self.root, text=self.transaction_handler.cash_machine.check_balance(), font=("Helvetica", 18), bg=GUIConstants.BACKGROUND_COLOR, fg=GUIConstants.TEXT_COLOR)
        self.balance_label.pack(pady=10)

        menu_frame = tk.Frame(self.root, bg=GUIConstants.BACKGROUND_COLOR)
        menu_frame.pack(pady=20)

        withdraw_button = tk.Button(menu_frame, text="Withdraw Money", command=self.withdraw_money, font=GUIConstants.FONT_STYLE, bg=GUIConstants.BUTTON_COLOR, fg=GUIConstants.TEXT_COLOR)
        withdraw_button.grid(row=0, column=0, padx=10, pady=10)

        deposit_button = tk.Button(menu_frame, text="Deposit Money", command=self.deposit_money, font=GUIConstants.FONT_STYLE, bg=GUIConstants.BUTTON_COLOR, fg=GUIConstants.TEXT_COLOR)
        deposit_button.grid(row=0, column=1, padx=10, pady=10)

        history_button = tk.Button(menu_frame, text="Show/Hide History", command=self.show_or_hide_history, font=GUIConstants.FONT_STYLE, bg=GUIConstants.BUTTON_COLOR, fg=GUIConstants.TEXT_COLOR)
        history_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        change_pin_button = tk.Button(menu_frame, text="Change PIN", command=self.change_pin, font=GUIConstants.FONT_STYLE, bg=GUIConstants.BUTTON_COLOR, fg=GUIConstants.TEXT_COLOR)
        change_pin_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.amount_entry = tk.Entry(menu_frame, font=GUIConstants.FONT_STYLE, width=20, justify="left", insertwidth=4, state="normal")
        self.amount_entry.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.amount_entry.insert(0, "Enter amount €")
        self.amount_entry.bind("<FocusIn>", self.clear_default_text)

        quit_button = tk.Button(self.root, text="Quit", command=self.quit_program, bg=GUIConstants.FAILURE_COLOR, fg=GUIConstants.TEXT_COLOR, font=GUIConstants.FONT_STYLE)
        quit_button.pack()

        self.history_frame = tk.Frame(self.root, bg=GUIConstants.BACKGROUND_COLOR)
        self.history_frame.pack(pady=20)

        self.history_text = tk.Text(self.history_frame, height=20, width=60, wrap=tk.WORD, font=("Helvetica", 12), bg=GUIConstants.TEXT_AREA_COLOR, fg=GUIConstants.TEXT_COLOR)
        self.history_text.pack()

    def show_or_hide_history(self):
        """Toggle showing or hiding transaction history in the GUI"""
        if not self.showing_history:
            self.update_history_text()
            self.showing_history = True
        else:
            self.history_text.delete(1.0, tk.END)
            self.showing_history = False

    def change_pin(self):
        """Prompt the user to change their PIN"""
        new_pin = simpledialog.askstring("Change PIN", "Enter your new 4-digit PIN:")
        if new_pin:
            if self.transaction_handler.cash_machine.set_pin(new_pin):
                messagebox.showinfo("PIN Changed", "PIN successfully changed!")
            else:
                messagebox.showerror("Error", "Invalid PIN. Please enter a 4-digit PIN.")

    def withdraw_or_deposit(self, transaction_type):
        """Perform withdrawal or deposit based on user input"""
        amount = self.get_amount()
        if amount is not None:
            confirmation = messagebox.askyesno("Transaction Confirmation", f"Are you sure you want to {transaction_type} {self.transaction_handler.cash_machine.format_currency(amount)}?")
            if confirmation:
                result, success = None, False
                if transaction_type == "withdraw":
                    result, success = self.transaction_handler.perform_withdrawal(amount)
                else:
                    result, success = self.transaction_handler.perform_deposit(amount)

                self.handle_transaction_result(result, success)

    def withdraw_money(self):
        """Wrapper function for withdrawing money"""
        self.withdraw_or_deposit("withdraw")

    def deposit_money(self):
        """Wrapper function for depositing money"""
        self.withdraw_or_deposit("deposit")

    def show_history(self):
        """Show the transaction history"""
        self.update_history_text()

    def quit_program(self):
        """Prompt user to confirm quitting the program"""
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.root.destroy()

    def clear_default_text(self, event):
        """Clear default text in the entry box when it is focused"""
        current_text = self.amount_entry.get()
        if current_text == "Enter amount €" or current_text.replace(".", "").isdigit():
            self.amount_entry.delete(0, tk.END)
        self.amount_entry.icursor("end")

    def get_amount(self):
        """Get the amount entered by the user, handle invalid inputs"""
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Invalid input. Amount must be greater than 0.")
                return None
            return amount
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid amount.")
            return None

    def handle_transaction_result(self, result, success):
        """Handle and display transaction results and errors"""
        if result is not None and success:
            messagebox.showinfo("Transaction Result", result)
            self.root.configure(bg=GUIConstants.SUCCESS_COLOR)
            self.root.after(1000, lambda: self.root.configure(bg=GUIConstants.BACKGROUND_COLOR))
            self.set_default_text()
        elif result is not None:
            if "Insufficient funds" in result:
                self.transaction_handler.cash_machine.transaction_history.append(result)
                self.update_balance_label()
                self.update_history_text()
                messagebox.showerror("Transaction Result", "Insufficient funds. Withdrawal amount exceeds the current balance.")
                self.root.configure(bg=GUIConstants.FAILURE_COLOR)
                self.root.after(1000, lambda: self.root.configure(bg=GUIConstants.BACKGROUND_COLOR))
            else:
                messagebox.showerror("Transaction Result", result)
                self.root.configure(bg=GUIConstants.FAILURE_COLOR)
                self.root.after(1000, lambda: self.root.configure(bg=GUIConstants.BACKGROUND_COLOR))

        self.update_balance_label()
        self.update_history_text()

    def update_balance_label(self):
        """Update the balance label in the GUI"""
        self.balance_label.config(text=self.transaction_handler.cash_machine.check_balance())

    def update_history_text(self):
        """Update the transaction history text in the GUI"""
        self.history_text.delete(1.0, tk.END)
        history_text = "\n".join(self.transaction_handler.cash_machine.transaction_history)
        self.history_text.insert(tk.END, history_text)

    def set_default_text(self):
        """Set default text in the entry box after a transaction"""
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, "Enter amount €")

# Main execution block
if __name__ == "__main__":
    # Set the locale for currency formatting
    locale.setlocale(locale.LC_ALL, '')

    # Create Tkinter root, CashMachine instance, and TransactionHandler instance
    root = tk.Tk()
    cash_machine = CashMachine()
    transaction_handler = TransactionHandler(cash_machine)

    # Create and run the CashMachineGUI
    app = CashMachineGUI(root, transaction_handler)
    root.mainloop()

import PySimpleGUI as sg

class CashMachine:
    def __init__(self):
        self.balance = 0

    def check_balance(self):
        return self.balance

    def withdraw_money(self, amount):
        self.balance -= amount

    def deposit_money(self, amount):
        self.balance += amount


cash_machine = CashMachine()

layout = [
    [sg.Text("CASH MACHINE MENU", font=("Arial", 18, "bold"))],
    [sg.Button("Check Balance", size=(20, 2))],
    [sg.Button("Withdraw Money", size=(20, 2))],
    [sg.Button("Deposit Money", size=(20, 2))],
    [sg.Button("Quit", size=(20, 2))],
    [sg.Text("", key="-OUTPUT-", size=(30, 2))]
]

window = sg.Window("Cash Machine", layout)

while True:
    event, values = window.read()
    if event == "Check Balance":
        cash_machine.check_balance()
        window["-OUTPUT-"].update(f"Your current balance is €{cash_machine.balance}")
    elif event == "Withdraw Money":
        amount = sg.popup_get_text("Enter the amount to withdraw: €")
        try:
            amount = float(amount)
            if cash_machine.balance < amount:
                window["-OUTPUT-"].update("Insufficient balance.")
            else:
                cash_machine.withdraw_money(amount)
                window["-OUTPUT-"].update(f"€{amount} has been withdrawn. Your new balance is €{cash_machine.balance}")
        except ValueError:
            window["-OUTPUT-"].update("Invalid amount.")
    elif event == "Deposit Money":
        amount = sg.popup_get_text("Enter the amount to deposit: €")
        try:
            amount = float(amount)
            cash_machine.deposit_money(amount)
            window["-OUTPUT-"].update(f"€{amount} has been deposited. Your new balance is €{cash_machine.balance}")
        except ValueError:
            window["-OUTPUT-"].update("Invalid amount.")
    elif event == "Quit" or event == None:
        break

window.close()

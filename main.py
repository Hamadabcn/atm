class CashMachine:
    def __init__(self):
        self.balance = 0

    def display_menu(self):
        print("""
            ************************
            *  CASH MACHINE MENU   *
            ************************
            1. Check Balance
            2. Withdraw Money
            3. Deposit Money
            4. Quit
            ************************
        """)

    def check_balance(self):
        print(f"\nYour current balance is €{self.balance}\n")

    def withdraw_money(self):
        amount = float(input("\nEnter the amount to withdraw: € "))
        if self.balance < amount:
            print("\nInsufficient balance.\n")
        else:
            self.balance -= amount
            print(f"\n€{amount} has been withdrawn. Your new balance is €{self.balance}\n")

    def deposit_money(self):
        amount = float(input("\nEnter the amount to deposit: € "))
        self.balance += amount
        print(f"\n€{amount} has been deposited. Your new balance is €{self.balance}\n")


cash_machine = CashMachine()

while True:
    cash_machine.display_menu()
    option = input("\nEnter your choice (1-4): ")

    if option == '1':
        cash_machine.check_balance()
    elif option == '2':
        cash_machine.withdraw_money()
    elif option == '3':
        cash_machine.deposit_money()
    elif option == '4':
        print("\nThank you for using the cash machine. Goodbye!\n")
        break
    else:
        print("\nInvalid option. Please try again.\n")
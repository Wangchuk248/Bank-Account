import time

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show_info(self):
        return f"Thank you, {self.name.title()}, {self.age} years old"

class Bank(User):
    total_deposit = 0
    total_withdraws = 0

    def __init__(self, name, age, balance, b_acc_no, ba_password, b_acc_type):
        super().__init__(name, age)
        self.balance = balance
        self.b_acc_no = b_acc_no
        self.ba_password = ba_password
        self.b_acc_type = b_acc_type

    def show_details(self):
        return f"{self.name} has a remaining balance of: {round(self.balance, 2)}"

    def deposit(self):
        dp = float(input(f"{self.name.title()}, please enter how much you would like to deposit: "))
        self.balance += dp
        Bank.total_deposit += dp
        print("Thank you for depositing...")
        return f"Your balance is now: {round(self.balance, 2)}"

    def withdraw(self):
        wd = float(input(f"{self.name.title()}, please enter how much you would like to withdraw: "))
        if self.balance < wd:
            return "Withdraw failed due to insufficient funds"
        else:
            self.balance -= wd
            Bank.total_withdraws += wd
            print("Thank you for withdrawing...")
            return f"Your balance is now: {round(self.balance, 2)}"

    def save_to_file(self, filename='b_acc.txt'):
        b_account_info = f"{self.name},{self.age},{self.b_acc_no},{self.ba_password},{self.b_acc_type},{self.balance}\n"
        with open(filename, 'a') as file:
            file.write(b_account_info)

    @staticmethod
    def load_from_file(b_acc_no, ba_password, filename='b_acc.txt'):
        with open(filename, 'r') as file:
            for line in file:
                name, age, acc_num, pwd, acc_type, balance = line.strip().split(',')
                if acc_num == b_acc_no and pwd == ba_password:
                    print("Login successful.")
                    return Bank(name, int(age), float(balance), acc_num, pwd, acc_type)
        print("Invalid account number or password.")
        return None
    
    @staticmethod
    def generate_account_number():
        current_time = str(int(time.time() * 1000))
        return current_time[-8:]

    def transfer_money(self, recipient_account):
        amount = float(input(f"How much money would you like to send to {recipient_account.name}? "))
        if self.balance < amount:
            return "Transfer failed due to insufficient funds"
        else:
            self.balance -= amount
            recipient_account.balance += amount
            print(f"Successfully sent {amount} to {recipient_account.name}.")
            return f"Your balance is now: {round(self.balance, 2)}"

def options(user_one_bank, all_accounts):
    print('Account created successfully.')
    print("Here are a few options, please choose the number you want")
    while True:
        options_choice = int(input("1) See balance\n2) Withdraw\n3) Deposit\n4) See total Deposits\n5) See Total Withdraws\n6) Send Money\n7) Logout\n"))
        if options_choice == 1:
            print(user_one_bank.show_details())
        elif options_choice == 2:
            print(user_one_bank.withdraw())
        elif options_choice == 3:
            print(user_one_bank.deposit())
        elif options_choice == 4:
            print(f"There have been {Bank.total_deposit} total deposits.")
        elif options_choice == 5:
            print(f"There have been {Bank.total_withdraws} total withdraws.")
        elif options_choice == 6:
            recipient_account_number = input("Enter the recipient's account number: ")
            recipient_account = next((acc for acc in all_accounts if acc.b_acc_no == recipient_account_number), None)
            if recipient_account:
                print(user_one_bank.transfer_money(recipient_account))
            else:
                print("Recipient account not found.")
        elif options_choice == 7:
            print("Thank you for using Ugyen's Bank")
            return True
        else:
            print("Please choose a number from 1-7.")

def bank_creation(name):
    balance = float(input(f"{name}, how much money do you have? "))
    return balance

all_accounts = []
while True:
    print("Welcome to Ugyen's bank")
    choice = input("1) Create Account\n2) Login\n3) Exit\nEnter choice: ")

    if choice == '1':
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        account_number = Bank.generate_account_number()
        password = input("Create a password: ")
        account_type = input("Enter account type (Personal/Business): ")
        balance = float(input("Enter initial deposit amount: "))
        user_one = Bank(name, age, balance, account_number, password, account_type)
        user_one.save_to_file()
        all_accounts.append(user_one)
        print(f"Account created. Account Number: {account_number}, Password: {password}")
        options_returned = options(user_one, all_accounts)
        if not options_returned:
            break
    elif choice == '2':
        account_number = input("Enter your account number: ")
        password = input("Enter your password: ")
        user_one = Bank.load_from_file(account_number, password)
        if user_one:
            options_returned = options(user_one, all_accounts)
            if not options_returned:
                break
    elif choice == '3':
        break
    else:
        print("Invalid choice. Please try again.")

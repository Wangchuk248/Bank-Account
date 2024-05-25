import time

class User:# Implements a class called User with two attributes 'name' and 'age'
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show_info(self):  # This method returns a string with the user's name and age.
        return f"Thank you, {self.name.title()}, {self.age} years old"

class Bank(User):# 'Bank' class inherits from the User class and represents a bank account.
    total_deposit = 0# Class variable tracks total deposits
    total_withdraws = 0# It also tracks total withdrawals

    def __init__(self, name, age, balance, b_acc_no, ba_password, b_acc_type):# Initializes attributes such as bank account number (b_acc_no), balance, and account type (b_acc_type)
        super().__init__(name, age)
        self.balance = balance
        self.b_acc_no = b_acc_no
        self.ba_password = ba_password
        self.b_acc_type = b_acc_type

    def show_details(self):  # Returns the account holder's name and remaining balance
        return f"{self.name} has a remaining balance of: {round(self.balance, 2)}"

    def deposit(self):  # Prompts the user to enter a deposit amount, updates the balance, and adds to the total deposits
        dp = float(input(f"{self.name.title()}, please enter how much you would like to deposit: "))
        self.balance += dp # Update balance with deposit amount
        Bank.total_deposit += dp# Update total deposits
        print("Thank you for depositing...")
        return f"Your balance is now: {round(self.balance, 2)}" # Display updated balance

    def withdraw(self):# Prompts the user to enter a withdrawal amount, checks for sufficient funds, updates the balance, and adds to the total withdrawals
        wd = float(input(f"{self.name.title()}, please enter how much you would like to withdraw: "))
        if self.balance < wd:# Checks if balance is sufficient
            return "Withdraw failed due to insufficient funds"
        else:
            self.balance -= wd  # Update balance with withdrawal amount
            Bank.total_withdraws += wd # Updates total withdrawals
            print("Thank you for withdrawing...")
            return f"Your balance is now: {round(self.balance, 2)}"# Display updated balance

    def save_to_file(self, filename='b_acc.txt'): # Saves the account details to a file
        b_account_info = f"{self.name},{self.age},{self.b_acc_no},{self.ba_password},{self.b_acc_type},{self.balance}\n"
        with open(filename, 'a') as file:
            file.write(b_account_info)

    @staticmethod # Static method to load account details from a file
    def load_from_file(b_acc_no, ba_password, filename='b_acc.txt'):
        with open(filename, 'r') as file:
            for line in file:
                name, age, acc_num, pwd, acc_type, balance = line.strip().split(',')
                if acc_num == b_acc_no and pwd == ba_password: # Check if account number and password matches. Else it prints error message.
                    print("Login successful.")
                    return Bank(name, int(age), float(balance), acc_num, pwd, acc_type)
        print("Invalid account number or password.")
        return None
    
    @staticmethod
    def generate_account_number():# Generates random account numbers
        current_time = str(int(time.time() * 1000))
        return current_time[-8:]# Use the last 8 digits as the account number

    def transfer_money(self, recipient_account): # Method to send money to another account
        amount = float(input(f"How much money would you like to send to {recipient_account.name}? "))
        if self.balance < amount:
            return "Transfer failed due to insufficient funds"
        else:
            self.balance -= amount
            recipient_account.balance += amount
            print(f"Successfully sent {amount} to {recipient_account.name}.")
            return f"Your balance is now: {round(self.balance, 2)}"
# Providing a menu for the user to interact with their own account
def options(user_one_bank, all_accounts):
    print('Account created successfully.')
    print("Here are a few options, please choose the number you want")
    while True: # Provides options for the user to see balance, withdraw, deposit, total deposits, total withdrawals, send money, and logout
        options_choice = int(input("1) See balance\n2) Withdraw\n3) Deposit\n4) See total Deposits\n5) See Total Withdraws\n6) Send Money\n7) Logout\n"))
        if options_choice == 1:#To see balance
            print(user_one_bank.show_details())
        elif options_choice == 2: #to withdraw money
            print(user_one_bank.withdraw())#display the amount withdrawed
        elif options_choice == 3:#to deposit the money 
            print(user_one_bank.deposit())#displays the amount deposited
        elif options_choice == 4:#to see the total deposits
            print(f"There have been {Bank.total_deposit} total deposits.")
        elif options_choice == 5:#to see the total withdraws
            print(f"There have been {Bank.total_withdraws} total withdraws.")
        elif options_choice == 6:#to send money to other account
            recipient_account_number = input("Enter the recipient's account number: ")
            recipient_account = next((acc for acc in all_accounts if acc.b_acc_no == recipient_account_number), None)#asks for reciepient's account number
            if recipient_account:
                print(user_one_bank.transfer_money(recipient_account))
            else:
                print("Recipient account not found.")
        elif options_choice == 7:#to logout
            print("Thank you for using Ugyen's Bank")
            return True
        else:
            print("Please choose a number from 1-7.")
# Starting the main program
def bank_creation(name):
    balance = float(input(f"{name}, how much money do you have? "))  # Prompts the user to enter their current balance and returns it
    return balance
# Main loop
all_accounts = []
while True: # Runs the main program, providing options to create an account, log in, or exit
    print("Welcome to Ugyen's bank")
    choice = input("1) Create Account\n2) Login\n3) Exit\nEnter choice: ")

    if choice == '1':
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        account_number = Bank.generate_account_number()# Generates a random account number
        password = input("Create a password: ")
        account_type = input("Enter account type (Personal/Business): ")
        balance = float(input("Enter initial deposit amount: "))
        user_one = Bank(name, age, balance, account_number, password, account_type)
        user_one.save_to_file()
        all_accounts.append(user_one) # Add the new account to the list of all accounts
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
    elif choice == '3':# Breaks the loop and exits the program
        break
    else:
        print("Invalid choice. Please try again.")# Prompts the user to try again if the input is invalid"

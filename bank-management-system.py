import json
import os

class BankAccount:
    def __init__(self, username, password, balance=0):
        self.username = username
        self.password = password
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Deposited: {amount}")
        print(f"The amount of {amount} has been deposited to your account.")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"Withdrawn: {amount}")
            print(f"An amount of {amount} has been withdrawn from your account.")
        else:
            print("Insufficient funds")

    def display_balance(self):
        print(f"The remaining balance in your account is {self.balance}")

    def display_transactions(self):
        if self.transactions:
            print("\nTransaction History:")
            for transaction in self.transactions:
                print(transaction)
        else:
            print("No transactions available.")


class BankSystem:
    def __init__(self, data_file='bank_data.json'):
        self.data_file = data_file
        self.accounts = self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                return {username: BankAccount(username, acc['password'], acc['balance']) 
                        for username, acc in data.items()}
        else:
            return {}

    def save_data(self):
        with open(self.data_file, 'w') as file:
            data = {username: {'password': acc.password, 'balance': acc.balance} 
                    for username, acc in self.accounts.items()}
            json.dump(data, file,indent=4)

    def create_account(self):
        username = input("Enter a new username: ")
        if username in self.accounts:
            print("Username already exists. Try again.")
            return
        password = input("Enter a new password: ")
        self.accounts[username] = BankAccount(username, password)
        print("Account created successfully!")

    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if username in self.accounts and self.accounts[username].password == password:
            print("Login successful!")
            return self.accounts[username]
        else:
            print("Invalid username or password.")
            return None

    def run(self):
        while True:
            print("\n1. Create Account\n2. Login\n3. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.create_account()
                self.save_data()
            elif choice == '2':
                user = self.login()
                if user:
                    while True:
                        print("\n1. View Balance\n2. Deposit\n3. Withdraw\n4. View Transactions\n5. Logout")
                        choice = input("Enter your choice: ")

                        if choice == '1':
                            user.display_balance()
                        elif choice == '2':
                            amount = int(input("Enter amount to deposit: "))
                            user.deposit(amount)
                            self.save_data()
                        elif choice == '3':
                            amount = int(input("Enter amount to withdraw: "))
                            user.withdraw(amount)
                            self.save_data()
                        elif choice == '4':
                            user.display_transactions()
                        elif choice == '5':
                            print("Logged out.")
                            break
                        else:
                            print("Invalid choice. Please try again.")
            elif choice == '3':
                print("Thank you for using the bank service. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")              

# Running the system
bank_system = BankSystem()
bank_system.run()

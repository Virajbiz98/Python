import tkinter as tk
from tkinter import messagebox

# Sample user data
users = {"user1": "password1", "user2": "password2"}

def login():
    username = entry_username.get()
    password = entry_password.get()
    if username in users and users[username] == password:
        messagebox.showinfo("Login", "Login Successful")
        open_banking_interface()
    else:
        messagebox.showerror("Login", "Invalid Username or Password")

def open_banking_interface():
    login_window.destroy()
    banking_interface()

# Login GUI setup
login_window = tk.Tk()
login_window.title("Login")

tk.Label(login_window, text="Username").pack()
entry_username = tk.Entry(login_window)
entry_username.pack()

tk.Label(login_window, text="Password").pack()
entry_password = tk.Entry(login_window, show="*")
entry_password.pack()

tk.Button(login_window, text="Login", command=login).pack()

login_window.mainloop()

class BankAccount:
    def __init__(self, account_holder, balance=0):
        self.account_holder = account_holder
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. New balance is {self.balance}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance is {self.balance}")
        else:
            print("Insufficient funds")

    def check_balance(self):
        print(f"Current balance is {self.balance}")
def transfer_money(sender, receiver, amount):
    if sender.balance >= amount:
        sender.withdraw(amount)
        receiver.deposit(amount)
        print(f"Transferred {amount} from {sender.account_holder} to {receiver.account_holder}")
    else:
        print("Insufficient funds for transfer")
def banking_interface():
    bank_window = tk.Tk()
    bank_window.title("Banking Interface")

    account1 = BankAccount("Alice", 1000)
    account2 = BankAccount("Bob", 500)

    def show_balance():
        messagebox.showinfo("Balance", f"Balance: {account1.balance}")

    def deposit_money():
        amount = int(entry_amount.get())
        account1.deposit(amount)
        show_balance()

    def withdraw_money():
        amount = int(entry_amount.get())
        account1.withdraw(amount)
        show_balance()

    def transfer_money_gui():
        amount = int(entry_amount.get())
        transfer_money(account1, account2, amount)
        show_balance()

    tk.Label(bank_window, text="Amount").pack()
    entry_amount = tk.Entry(bank_window)
    entry_amount.pack()

    tk.Button(bank_window, text="Deposit", command=deposit_money).pack()
    tk.Button(bank_window, text="Withdraw", command=withdraw_money).pack()
    tk.Button(bank_window, text="Transfer", command=transfer_money_gui).pack()
    tk.Button(bank_window, text="Check Balance", command=show_balance).pack()

    bank_window.mainloop()
# Place the login and banking interface code here

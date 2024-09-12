import tkinter as tk
from tkinter import * 
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import ttk

# Define data structures for accounts, transactions, and blocks.
class Account:
    def __init__(self, address, balance):
        self.address = address
        self.balance = balance

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

class Block:
    def __init__(self, staker, value):
        self.staker = staker
        self.value = value

# Create lists to store accounts, pending transactions, and the blockchain.
accounts = []
pending_transactions = []
blockchain = []

# Create a Tkinter GUI.
window = Tk()
window.title("Crypto Exchange Simulator")
window.geometry('800x650')

def create_account_starting(add):
    address = add
    initial_balance = 100000.0
    accounts.append(Account(address, initial_balance))

create_account_starting('112A')
create_account_starting('112B')
create_account_starting('112C')
create_account_starting('112D')
create_account_starting('112E')

# Function to create a new account.
def create_account():
    address = account_entry.get()
    initial_balance_str = balance_entry.get()
    
    # Validate that the initial_balance_str is not empty and can be converted to a float.
    if not initial_balance_str:
        update_status("Please enter a valid initial balance.")
        return
    
    try:
        initial_balance = float(initial_balance_str)
    except ValueError:
        update_status("Invalid initial balance. Please enter a valid number.")
        return
    
    accounts.append(Account(address, initial_balance))
    account_entry.delete(0, tk.END)
    balance_entry.delete(0, tk.END)
    update_status("Account created successfully.")

# Function to initiate a transaction.
def initiate_transaction():
    sender = sender_entry.get()
    receiver = receiver_entry.get()
    amount = float(amount_entry.get())
    transaction = Transaction(sender, receiver, amount)
    pending_transactions.append(transaction)
    sender_entry.delete(0, tk.END)
    receiver_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    update_status("Transaction initiated. Pending approval.")


# Function to validate and commit a transaction.
def commit_transaction():
    global pending_transactions
    if not pending_transactions:
        return
    transaction = pending_transactions[0]
    sender_account = next((acc for acc in accounts if acc.address == transaction.sender), None)
    receiver_account = next((acc for acc in accounts if acc.address == transaction.receiver), None)
    
    if sender_account and receiver_account and sender_account.balance >= transaction.amount:
        sender_account.balance -= transaction.amount
        receiver_account.balance += transaction.amount
        pending_transactions = pending_transactions[1:]  # Remove the first element
        update_transaction_list()  # Update the transaction list in the GUI
        update_status("Transaction committed successfully.")
    elif sender_account and receiver_account not in accounts:
        update_status("Transaction failed. Foreign account(s).")
        pending_transactions.clear()
    else:
        update_status("Transaction failed. Insufficient balance.")
        pending_transactions.clear()
def mine_block():
    if len(blockchain) < 1:
        messagebox.showerror("Error", "No stakers found.")
        return

    # Find the winner based on the highest stake
    winner_staker = None
    highest_stake = 0
    for block in blockchain:
        if block.value > highest_stake:
            highest_stake = float(block.value)
            winner_staker = block.staker

    # Check if the winner staker is in the accounts list
    winner_found = False
    for acc in accounts:
        if acc.address == winner_staker:
            acc.balance += float(highest_stake)
            winner_found = True
            break

    # Clear the blockchain
    blockchain.clear()

    # Update the status
    if winner_found:
        update_status(f"Block mined successfully. Winner: {winner_staker}. Reward ad: {highest_stake}.")
    else:
        update_status("Foreign account detected, so action declined")

#Function to update the status label.
def update_status(message):
    status_label.config(text=message)

# Function to update the accounts list.
def update_accounts_list():
    for i in accounts_tree.get_children():
        accounts_tree.delete(i)

    for acc in accounts:
        accounts_tree.insert("", "end", values=(acc.address,acc.balance))

# Function to update the transaction list.
def update_transaction_list():
    for i in transaction_tree.get_children():
        transaction_tree.delete(i)

    for j in pending_transactions:
        transaction_tree.insert("", "end", values=(j.sender,j.receiver,j.amount))

# Function to update the stakers list.
def update_stakers_list():
    for i in stakers_tree.get_children():
        stakers_tree.delete(i)

    for k in blockchain:
        stakers_tree.insert("", "end", values=(k.staker,k.value))

# Function to Add the stakers into the list.
def add_staker_function():
    staker_address = Address_entry.get()
    staker_amount = float(Amount_entry.get())
    blockchain.append(Block(staker_address, staker_amount))
    Address_entry.delete(0, tk.END)
    Amount_entry.delete(0, tk.END)
    update_stakers_list()

# Update the stakers list in the GUI


#GUI
#########################################################################################################################

tabs_control = Notebook(window)
create_account_tab = Frame(tabs_control)
send_money_tab = Frame(tabs_control)
mining_tab = Frame(tabs_control)

#TABS
tabs_control.add(create_account_tab, text="Create account")
tabs_control.add(send_money_tab, text="Send money")
tabs_control.add(mining_tab, text='Mining section')
tabs_control.pack(expand = 1, fill ="both")

#Labels and input fields for account creation.
account_label = Label(create_account_tab, text="Account Address:")
account_label.pack()
account_entry = Entry(create_account_tab)
account_entry.pack()

balance_label = tk.Label(create_account_tab, text="Initial Balance:")
balance_label.pack()
balance_entry = tk.Entry(create_account_tab)
balance_entry.pack()

create_account_button = tk.Button(create_account_tab, text="Create Account", command=lambda: [create_account(), update_accounts_list()])
create_account_button.pack()

# Labels and input fields for transaction initiation.
sender_label = tk.Label(send_money_tab, text="Sender:")
sender_label.pack()
sender_entry = tk.Entry(send_money_tab)
sender_entry.pack()

receiver_label = tk.Label(send_money_tab, text="Receiver:")
receiver_label.pack()
receiver_entry = tk.Entry(send_money_tab)
receiver_entry.pack()

amount_label = tk.Label(send_money_tab, text="Amount:")
amount_label.pack()
amount_entry = tk.Entry(send_money_tab)
amount_entry.pack()

initiate_transaction_button = tk.Button(send_money_tab, text="Initiate Transaction", command=initiate_transaction)
initiate_transaction_button.pack()
commit_transaction_button = tk.Button(send_money_tab, text="Commit Transaction", command=commit_transaction)

#to display list of accounts
accounts_tree = ttk.Treeview(create_account_tab, columns=("Address", "Balance"), show="headings")
accounts_tree.heading("Address", text="Account Address")
accounts_tree.heading("Balance", text="Current Balance")
accounts_tree.column("Address", width=150)
accounts_tree.column("Balance", width=100)
accounts_tree.pack()

#to display pending transactions
transaction_tree = ttk.Treeview(send_money_tab, columns=("Sender", "Receiver","Amount"), show="headings")
transaction_tree.heading("Sender", text="Sender")
transaction_tree.heading("Receiver", text="Receiver")
transaction_tree.heading("Amount", text="Amount")
transaction_tree.column("Sender", width=100)
transaction_tree.column("Receiver", width=100)
transaction_tree.column("Amount", width=100)
transaction_tree.pack()


#refresh for create_acc_tab
refresh_button = tk.Button(create_account_tab, text="Refresh list", command=update_accounts_list)
refresh_button.pack()

#refresh for send_money_tab
refresh_button = tk.Button(send_money_tab, text="Refresh list", command=update_transaction_list)
refresh_button.pack()
commit_transaction_button.pack()


#put in miner section
Address_label = tk.Label(mining_tab, text="Address of staker")
Address_label.pack()
Address_entry = tk.Entry(mining_tab)
Address_entry.pack()

amount_label = tk.Label(mining_tab, text="Amount staked")
amount_label.pack()
Amount_entry = tk.Entry(mining_tab)
Amount_entry.pack()

ADD_button = tk.Button(mining_tab, text="ADD", command=add_staker_function)
ADD_button.pack()


#to display stakers
stakers_tree = ttk.Treeview(mining_tab, columns=("Address of staker","Amount staked"), show="headings")
stakers_tree.heading("Address of staker", text="Address of staker")
stakers_tree.heading("Amount staked", text="Amount staked")
stakers_tree.column("Address of staker", width=150)
stakers_tree.column("Amount staked", width=150)
stakers_tree.pack()
#refresh for mining_tab
refresh_button = tk.Button(mining_tab, text="Refresh list", command=update_stakers_list)
refresh_button.pack()

mine_block_button = tk.Button(mining_tab, text="Mine Block", command=mine_block)
mine_block_button.pack()
# Status label.
status_label = tk.Label(tabs_control, text="", fg="green")
status_label.pack()

window.mainloop()
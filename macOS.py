from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget, QWidget
import sys
import random

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

# Initialize a few sample accounts with starting balances.
def create_account_starting(add):
    address = add
    initial_balance = 100000.0
    accounts.append(Account(address, initial_balance))

create_account_starting('112A')
create_account_starting('112B')
create_account_starting('112C')
create_account_starting('112D')
create_account_starting('112E')

# Blockchain GUI application with tabs.
class BlockchainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crypto Exchange Simulator")
        self.setGeometry(200, 200, 800, 600)

        # Main layout and tab widget
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        # Create Account tab
        self.create_account_tab = QWidget()
        self.create_account_layout = QVBoxLayout(self.create_account_tab)
        self.tabs.addTab(self.create_account_tab, "Create Account")

        # Transaction tab
        self.transaction_tab = QWidget()
        self.transaction_layout = QVBoxLayout(self.transaction_tab)
        self.tabs.addTab(self.transaction_tab, "Transaction")

        # Mine Block tab
        self.mine_block_tab = QWidget()
        self.mine_block_layout = QVBoxLayout(self.mine_block_tab)
        self.tabs.addTab(self.mine_block_tab, "Mine Block")

        # Call methods to set up each tab's content
        self.setup_create_account_tab()
        self.setup_transaction_tab()
        self.setup_mine_block_tab()

    def setup_create_account_tab(self):
        # Account creation fields
        self.account_label = QLabel("Create Account:")
        self.create_account_layout.addWidget(self.account_label)
        self.account_entry = QLineEdit(self)
        self.account_entry.setPlaceholderText("Account Address")
        self.create_account_layout.addWidget(self.account_entry)

        self.balance_entry = QLineEdit(self)
        self.balance_entry.setPlaceholderText("Initial Balance")
        self.create_account_layout.addWidget(self.balance_entry)

        self.create_account_button = QPushButton("Create Account", self)
        self.create_account_button.clicked.connect(self.create_account)
        self.create_account_layout.addWidget(self.create_account_button)

        # Account list table
        self.accounts_table = QTableWidget(self)
        self.accounts_table.setColumnCount(2)
        self.accounts_table.setHorizontalHeaderLabels(["Address", "Balance"])
        self.create_account_layout.addWidget(self.accounts_table)

        self.update_accounts_list()

    def setup_transaction_tab(self):
        # Transaction fields
        self.sender_label = QLabel("Initiate Transaction:")
        self.transaction_layout.addWidget(self.sender_label)
        self.sender_entry = QLineEdit(self)
        self.sender_entry.setPlaceholderText("Sender Address")
        self.transaction_layout.addWidget(self.sender_entry)

        self.receiver_entry = QLineEdit(self)
        self.receiver_entry.setPlaceholderText("Receiver Address")
        self.transaction_layout.addWidget(self.receiver_entry)

        self.amount_entry = QLineEdit(self)
        self.amount_entry.setPlaceholderText("Amount")
        self.transaction_layout.addWidget(self.amount_entry)

        self.initiate_transaction_button = QPushButton("Initiate Transaction", self)
        self.initiate_transaction_button.clicked.connect(self.initiate_transaction)
        self.transaction_layout.addWidget(self.initiate_transaction_button)

        self.commit_transaction_button = QPushButton("Commit Transaction", self)
        self.commit_transaction_button.clicked.connect(self.commit_transaction)
        self.transaction_layout.addWidget(self.commit_transaction_button)

        # Transaction list table
        self.transactions_table = QTableWidget(self)
        self.transactions_table.setColumnCount(3)
        self.transactions_table.setHorizontalHeaderLabels(["Sender", "Receiver", "Amount"])
        self.transaction_layout.addWidget(self.transactions_table)

        self.update_transactions_list()

    def setup_mine_block_tab(self):
        # Staker fields
        self.staker_label = QLabel("Staking Section:")
        self.mine_block_layout.addWidget(self.staker_label)
        self.staker_address_entry = QLineEdit(self)
        self.staker_address_entry.setPlaceholderText("Staker Address")
        self.mine_block_layout.addWidget(self.staker_address_entry)

        self.staker_amount_entry = QLineEdit(self)
        self.staker_amount_entry.setPlaceholderText("Staked Amount")
        self.mine_block_layout.addWidget(self.staker_amount_entry)

        self.add_staker_button = QPushButton("Add Staker", self)
        self.add_staker_button.clicked.connect(self.add_staker)
        self.mine_block_layout.addWidget(self.add_staker_button)

        self.mine_block_button = QPushButton("Mine Block", self)
        self.mine_block_button.clicked.connect(self.mine_block)
        self.mine_block_layout.addWidget(self.mine_block_button)

        # Staker list table
        self.stakers_table = QTableWidget(self)
        self.stakers_table.setColumnCount(2)
        self.stakers_table.setHorizontalHeaderLabels(["Staker", "Amount Staked"])
        self.mine_block_layout.addWidget(self.stakers_table)

        self.update_stakers_list()

    def create_account(self):
        address = self.account_entry.text()
        initial_balance = self.balance_entry.text()
        result = create_account(address, initial_balance)
        self.update_accounts_list()
        self.show_message(result)
        if "successfully" in result:
            self.account_entry.clear()
            self.balance_entry.clear()


    def initiate_transaction(self):
        sender = self.sender_entry.text()
        receiver = self.receiver_entry.text()
        amount = self.amount_entry.text()
        result = initiate_transaction(sender, receiver, amount)
        self.update_transactions_list()
        self.show_message(result)

    def commit_transaction(self):
        result = commit_transaction()
        self.update_transactions_list()
        self.update_accounts_list()
        self.show_message(result)

    def add_staker(self):
        staker_address = self.staker_address_entry.text()
        staker_amount = self.staker_amount_entry.text()
        result = add_staker(staker_address, staker_amount)
        self.update_stakers_list()
        self.show_message(result)

    def mine_block(self):
        result = mine_block()
        self.update_accounts_list()
        self.update_stakers_list()
        self.show_message(result)

    def update_accounts_list(self):
        self.accounts_table.setRowCount(len(accounts))
        for i, acc in enumerate(accounts):
            self.accounts_table.setItem(i, 0, QTableWidgetItem(acc.address))
            self.accounts_table.setItem(i, 1, QTableWidgetItem(str(acc.balance)))

    def update_transactions_list(self):
        self.transactions_table.setRowCount(len(pending_transactions))
        for i, trans in enumerate(pending_transactions):
            self.transactions_table.setItem(i, 0, QTableWidgetItem(trans.sender))
            self.transactions_table.setItem(i, 1, QTableWidgetItem(trans.receiver))
            self.transactions_table.setItem(i, 2, QTableWidgetItem(str(trans.amount)))

    def update_stakers_list(self):
        self.stakers_table.setRowCount(len(blockchain))
        for i, block in enumerate(blockchain):
            self.stakers_table.setItem(i, 0, QTableWidgetItem(block.staker))
            self.stakers_table.setItem(i, 1, QTableWidgetItem(str(block.value)))

    def show_message(self, message):
        msg = QMessageBox()
        msg.setText(message)
        msg.exec_()

# Functionality unchanged from original code.
def create_account(address, initial_balance):
    try:
        initial_balance = float(initial_balance)
        accounts.append(Account(address, initial_balance))
        return "Account created successfully."
    except ValueError:
        return "Invalid initial balance. Please enter a valid number."

def initiate_transaction(sender, receiver, amount):
    try:
        amount = float(amount)
        transaction = Transaction(sender, receiver, amount)
        pending_transactions.append(transaction)
        return "Transaction initiated. Pending approval."
    except ValueError:
        return "Invalid amount. Please enter a valid number."

def commit_transaction():
    global pending_transactions
    if not pending_transactions:
        return "No pending transactions."
    
    transaction = pending_transactions[0]
    sender_account = next((acc for acc in accounts if acc.address == transaction.sender), None)
    receiver_account = next((acc for acc in accounts if acc.address == transaction.receiver), None)
    
    if sender_account and receiver_account and sender_account.balance >= transaction.amount:
        sender_account.balance -= transaction.amount
        receiver_account.balance += transaction.amount
        pending_transactions = pending_transactions[1:]
        return "Transaction committed successfully."
    elif sender_account and receiver_account not in accounts:
        pending_transactions.clear()
        return "Transaction failed. Foreign account(s)."
    else:
        pending_transactions.clear()
        return "Transaction failed. Insufficient balance"

def add_staker(staker_address, staker_amount):
    try:
        staker_amount = float(staker_amount)
        if staker_amount >=10000:
            blockchain.append(Block(staker_address, staker_amount))
            return "Staker added successfully."
        else:
            return "Staker amount too low."
    except ValueError:
        return "Invalid amount. Please enter a valid number."

def mine_block():
    if not blockchain:
        return "No stakers available for mining."
    reward = random.randint(199, 999)
    highest_staker = max(blockchain, key=lambda b: b.value)
    staker_account = next((acc for acc in accounts if acc.address == highest_staker.staker), None)
    
    if staker_account:
        staker_account.balance += reward  # Reward
        blockchain.clear()
        return f"Block mined successfully by {highest_staker.staker}. Reward: {reward} added to balance."
    else:
        return "Mining failed. Invalid staker."

# Main entry point for the application.
def main():
    app = QApplication(sys.argv)
    window = BlockchainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
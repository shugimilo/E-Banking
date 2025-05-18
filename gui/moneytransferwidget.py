import tkinter as tk
from tkinter import ttk
from classes.account import Account
from utils.fetcher import Fetcher
from tkinter.font import Font
from tkinter import messagebox

class MoneyTransferWidget(tk.Toplevel):
    def __init__(self, parent, account:Account):
        super().__init__(parent)
        self.title("Money Transfers")
        self.geometry("900x400")
        self.parent = parent
        self.account:Account = account
        self.money_transfers = account.money_transfers
        self.font = Font(family="Courier New", size=12)
        self.transfers_received = []
        self.transfers_sent = []
        self.split_money_transfers()

        self.main_frame = tk.Frame(self)
        self.main_frame.pack()

        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=1)

        self.sent_frame = ttk.Frame(self.notebook)
        self.sent_headers = ["Sent to", "Account Number", "Amount", "Currency", "Payment Purpose", "Transfer Date"]

        for column, header in enumerate(self.sent_headers):
            tk.Label(self.sent_frame, text=header, font=("Courier New", 12, "bold")).grid(row=0, column=column, padx=10, pady=5)

        self.process_sent_transfers()
        self.notebook.add(self.sent_frame, text="Sent")

        
        self.received_frame = ttk.Frame(self.notebook)
        self.received_headers = ["Received from", "Account Number", "Amount", "Currency", "Payment Purpose", "Transfer Date"]
        
        for column, header in enumerate(self.received_headers):
            tk.Label(self.received_frame, text=header, font=("Courier New", 12, "bold")).grid(row=0, column=column, padx=10, pady=5)
        
        self.process_received_transfers()
        self.notebook.add(self.received_frame, text="Received")

        self.new_frame = ttk.Frame(self.notebook)
        self.new_labels = ["Account Number", "Recipient Name", "Recipient Address", "Recipient City", "Payment Code", "Model", "Reference Number", "Payment Purpose"]

        for column, label in enumerate(self.new_labels):
            if column < 4:
                tk.Label(self.new_frame, text=label, font=("Courier New", 12, "bold")).grid(row=0, column=column, padx=20, pady=5)
            else:
                tk.Label(self.new_frame, text=label, font=("Courier New", 12, "bold")).grid(row=2, column=column-4, padx=20, pady=5)
        
        amount_label = tk.Label(self.new_frame, text=f"Amount ({self.account.currency})", font=("Courier New", 12, "bold"))
        amount_label.grid(row=4, column=0, padx=20, pady=5)

        self.account_number_entry = tk.Entry(self.new_frame)
        self.account_number_entry.grid(row=1, column=0, padx=10, pady=5)
        self.recipient_name_entry = tk.Entry(self.new_frame)
        self.recipient_name_entry.grid(row=1, column=1, padx=10, pady=5)
        self.recipient_address_entry = tk.Entry(self.new_frame)
        self.recipient_address_entry.grid(row=1, column=2, padx=10, pady=5)
        self.recipient_city_entry = tk.Entry(self.new_frame)
        self.recipient_city_entry.grid(row=1, column=3, padx=10, pady=5)
        self.payment_code_entry = tk.Entry(self.new_frame)
        self.payment_code_entry.grid(row=3, column=0, padx=10, pady=5)
        self.model_entry = tk.Entry(self.new_frame)
        self.model_entry.grid(row=3, column=1, padx=10, pady=5)
        self.reference_number_entry = tk.Entry(self.new_frame)
        self.reference_number_entry.grid(row=3, column=2, padx=10, pady=5)
        self.payment_purpose_entry = tk.Entry(self.new_frame)
        self.payment_purpose_entry.grid(row=3, column=3, padx=10, pady=5)
        self.amount_entry = tk.Entry(self.new_frame)
        self.amount_entry.grid(row=5, column=0, padx=10, pady=5)

        confirm_btn = tk.Button(self.new_frame, text="Confirm", font=self.font, command=self.confirm_money_transfer)
        confirm_btn.grid(row=5, column=1, padx=20, pady=5)
        cancel_btn = tk.Button(self.new_frame, text="Cancel", font=self.font, command=self.destroy)
        cancel_btn.grid(row=5, column=2, padx=20, pady=5)

        self.notebook.add(self.new_frame, text="New")

    def split_money_transfers(self):
        for transfer in self.money_transfers:
            if transfer.receiver_account_id == self.account.account_id:
                self.transfers_received.append(transfer)
            else:
                self.transfers_sent.append(transfer)

    def process_sent_transfers(self):
        fetcher = Fetcher()
        for row, transfer in enumerate(self.transfers_sent, start=1):
            fetched_user = fetcher.fetchUserInfoByAccountID(transfer.receiver_account_id)
            receiving_user_full_name = fetched_user["first_name"] + " " + fetched_user["last_name"]
            tk.Label(self.sent_frame, text=f"{receiving_user_full_name}", font=self.font).grid(row=row, column=0, padx=10, pady=5)
            receiving_account = Account.fetch_other_account(receiving_user_full_name, self.account.currency)
            tk.Label(self.sent_frame, text=f"{receiving_account.account_number}", font=self.font).grid(row=row, column=1, padx=10, pady=5)
            tk.Label(self.sent_frame, text=f"{transfer.amount}", font=self.font).grid(row=row, column=2, padx=10, pady=5)
            tk.Label(self.sent_frame, text=f"{self.account.currency}", font=self.font).grid(row=row, column=3, padx=10, pady=5)
            tk.Label(self.sent_frame, text=f"{transfer.payment_purpose}", font=self.font).grid(row=row, column=4, padx=10, pady=5)
            tk.Label(self.sent_frame, text=f"{transfer.transfer_date}", font=self.font).grid(row=row, column=5, padx=10, pady=5)

    def process_received_transfers(self):
        fetcher = Fetcher()
        for row, transfer in enumerate(self.transfers_received, start=1):
            fetched_user = fetcher.fetchUserInfoByAccountID(transfer.sender_account_id)
            sending_user_full_name = fetched_user["first_name"] + " " + fetched_user["last_name"]
            tk.Label(self.received_frame, text=f"{sending_user_full_name}", font=self.font).grid(row=row, column=0, padx=10, pady=5)
            sending_account = Account.fetch_other_account(sending_user_full_name, self.account.currency)
            tk.Label(self.received_frame, text=f"{sending_account.account_number}", font=self.font).grid(row=row, column=1, padx=10, pady=5)
            tk.Label(self.received_frame, text=f"{transfer.amount}", font=self.font).grid(row=row, column=2, padx=10, pady=5)
            tk.Label(self.received_frame, text=f"{self.account.currency}", font=self.font).grid(row=row, column=3, padx=10, pady=5)
            tk.Label(self.received_frame, text=f"{transfer.payment_purpose}", font=self.font).grid(row=row, column=4, padx=10, pady=5)
            tk.Label(self.received_frame, text=f"{transfer.transfer_date}", font=self.font).grid(row=row, column=5, padx=10, pady=5)

    def confirm_money_transfer(self):
        fetcher = Fetcher()
        if (self.account_number_entry.get()):
            recipient_account_number = self.account_number_entry.get()
            if(self.recipient_name_entry.get()):
                recipient_name = self.recipient_name_entry.get()
                if(self.recipient_address_entry.get()):
                    recipient_address = self.recipient_address_entry.get()
                    if(self.recipient_city_entry.get()):
                        recipient_city = self.recipient_city_entry.get()
                        if(self.payment_code_entry.get()):
                            payment_code = self.payment_code_entry.get()
                            if(self.model_entry.get()):
                                model = self.model_entry.get()
                                if(self.reference_number_entry.get()):
                                    reference_number = self.reference_number_entry.get()
                                    if(self.payment_purpose_entry.get()):
                                        payment_purpose = self.payment_purpose_entry.get()
                                        if(self.amount_entry.get()):
                                            amount = float(self.amount_entry.get())
                                            if(fetcher.checkIfUserExists(recipient_name)):
                                                recipient_account = Account.fetch_other_account(recipient_name, self.account.currency)
                                                if recipient_account_number != recipient_account.account_number:
                                                    messagebox.showinfo(title="Error", message="Recipient name and account number do not match.")
                                                else:
                                                    if amount > self.account.balance:
                                                        messagebox.showinfo(title="Error", message="Amount exceeds your account balance.")
                                                    else:
                                                        self.account.transfer_money(recipient_account, amount, recipient_name, recipient_address, recipient_city, payment_code, model, reference_number, payment_purpose)
                                                        messagebox.showinfo(title="Success", message="Transaction successful.")
                                                        self.parent.reload()
                                                        self.destroy()
                                            else:
                                                messagebox.showinfo(title="Error", message="There are no users with that name.")
                                        else:
                                            messagebox.showinfo(title="Error", message="You left the amount field empty.")
                                    else:
                                        messagebox.showinfo(title="Error", message="You left the payment purpose field empty.")
                                else:
                                    messagebox.showinfo(title="Error", message="You left the reference number field empty.")
                            else:
                                messagebox.showinfo(title="Error", message="You left the model field empty.")
                        else:
                            messagebox.showinfo(title="Error", message="You left the payment code field empty.")
                    else:
                        messagebox.showinfo(title="Error", message="You left the recipient city field empty.")
                else:
                    messagebox.showinfo(title="Error", message="You left the recipient address field empty.")
            else:
                messagebox.showinfo(title="Error", message="You left the recipient name field empty.")
        else:
            messagebox.showinfo(title="Error", message="You left the recipient account number field empty.")
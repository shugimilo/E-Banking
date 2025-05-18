import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from classes.account import Account
from functools import partial
from classes.bill import Bill
from tkinter import messagebox

class BillWidget(tk.Toplevel):
    def __init__(self, parent, account:Account):
        super().__init__(parent)
        self.parent = parent
        self.title("Bills")
        self.geometry("900x400")
        self.account:Account = account
        self.bills = account.bills
        self.bill_payments = account.bill_payments
        self.font = Font(family="Courier New", size=12)

        self.main_frame = tk.Frame(self)
        self.main_frame.pack()

        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=1)

        self.bills_frame = ttk.Frame(self.notebook)
        self.bill_payments_frame = ttk.Frame(self.notebook)
        
        bill_payment_headers = ["Biller Name", "Amount Paid", "Payment Date"]
        for i, header in enumerate(bill_payment_headers):
            header_label = tk.Label(self.bill_payments_frame, text=header, font=("Courier New", 14, "bold")).grid(row=0, column=i, padx=10, pady=5)
        
        for row, bill_payment in enumerate(self.bill_payments, start=1):
            tk.Label(self.bill_payments_frame, text=bill_payment.biller_name, font=self.font).grid(row=row, column=0, padx=10, pady=5)
            tk.Label(self.bill_payments_frame, text=(str(bill_payment.amount_paid) + " " + self.account.currency), font=self.font).grid(row=row, column=1, padx=10, pady=5)
            tk.Label(self.bill_payments_frame, text=bill_payment.payment_date, font=self.font).grid(row=row, column=2, padx=10, pady=5)

        self.process_bills()

        self.notebook.add(self.bills_frame, text="Bills")
        self.notebook.add(self.bill_payments_frame, text="Bill Payments")

    def process_bills(self):
        bill_headers = ["Biller Name", "Bill Amount", "Due Date", "Status", "Payment Date", "Action"]
        for column, header in enumerate(bill_headers):
            tk.Label(self.bills_frame, text=header, font=("Courier New", 14, "bold")).grid(row=0, column=column, padx=10, pady=5)
        for row, bill in enumerate(self.bills, start=1):
            tk.Label(self.bills_frame, text=bill.biller_name, font=self.font).grid(row=row, column=0, padx=10, pady=5)
            tk.Label(self.bills_frame, text=(str(bill.bill_amount) + " " + self.account.currency), font=self.font).grid(row=row, column=1, padx=10, pady=5)
            tk.Label(self.bills_frame, text=bill.due_date, font=self.font).grid(row=row, column=2, padx=10, pady=5)
            tk.Label(self.bills_frame, text=bill.status, font=self.font).grid(row=row, column=3, padx=10, pady=5)
            if bill.payment_date:
                if bill.status == "paid":
                    tk.Label(self.bills_frame, text=bill.payment_date, font=self.font).grid(row=row, column=4, padx=10, pady=5)
                else:
                    tk.Label(self.bills_frame, text="Not Paid Yet", font=self.font).grid(row=row, column=4, padx=10, pady=5)
            if bill.status == "paid":
                tk.Label(self.bills_frame, text="None", font=self.font).grid(row=row, column=5, padx=10, pady=5)
            else:
                tk.Button(self.bills_frame, text="Pay", font=self.font, command=partial(self.pay_bill, bill)).grid(row=row, column=5, padx=10, pady=5)

    def pay_bill(self, bill:Bill):
        message = self.account.pay_bill(self.account.cards[0], bill)
        if message != "Success.":
            messagebox.showinfo(title="Bill Payment Error", message=message)
        else:
            messagebox.showinfo(title="Bill Payment Status", message=message)
            self.parent.reload()
            self.destroy()

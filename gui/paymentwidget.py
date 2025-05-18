from classes.account import Account
import tkinter as tk
from tkinter.font import Font

class PaymentWidget(tk.Toplevel):
    def __init__(self, parent, account: Account):
        super().__init__(parent)
        self.account:Account = account
        self.title("Payments")
        self.geometry("600x400")
        self.font = Font(family="Courier New", size=12)

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(pady=10, padx=10)

        headers = ["Amount Paid", "Paid To", "Payment Date"]
        for i, header in enumerate(headers):
            header_label = tk.Label(self.main_frame, text=header, font=("Courier New", 14, "bold"))
            header_label.grid(row=0, column=i, padx=10, pady=5)

        for row, payment in enumerate(self.account.payments, start=1):
            tk.Label(self.main_frame, text=(str(payment.amount_paid) + " " + self.account.currency), font=self.font).grid(row=row, column=0, padx=10, pady=5)
            tk.Label(self.main_frame, text=payment.paid_to, font=self.font).grid(row=row, column=1, padx=10, pady=5)
            tk.Label(self.main_frame, text=str(payment.payment_date), font=self.font).grid(row=row, column=2, padx=10, pady=5)


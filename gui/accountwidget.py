import tkinter as tk
from tkinter.font import Font
from PIL import Image, ImageTk
from classes.account import Account
from gui.cardwidget import CardWidget
from gui.paymentwidget import PaymentWidget
from gui.billwidget import BillWidget
from gui.savingwidget import SavingWidget
from gui.moneytransferwidget import MoneyTransferWidget
from gui.exchangewidget import ExchangeWidget

class AccountWidget(tk.Frame):
    def __init__(self, parent, mainmenu, account:Account):
        super().__init__(parent)
        self.parent = mainmenu
        self.account:Account = account
        self.font1 = Font(family="Courier New", size=14, weight="bold")
        self.font2 = Font(family="Courier New", size=11, weight="bold")
        self.card_widget = CardWidget(self, self.account.cards[0])
        self.card_widget.pack(padx=10, pady=5)

        self.create_account_info()

        self.btn_frame = tk.Frame(self)
        payment_btn = tk.Button(self.btn_frame, text="Payments", bg="#2b2b2b", fg="white", font=self.font2, command=self.create_payment_widget, width=18)
        payment_btn.grid(row=0, column=0, padx=2, pady=2)
        bill_btn = tk.Button(self.btn_frame, text="Bills", bg="#2b2b2b", fg="white", font=self.font2, command=self.create_bill_widget, width=18)
        bill_btn.grid(row=0, column=1, padx=2, pady=2)
        saving_btn = tk.Button(self.btn_frame, text="Savings", bg="#2b2b2b", fg="white", font=self.font2, command=self.create_saving_widget, width=18)
        saving_btn.grid(row=1, column=0, padx=2, pady=2)
        money_transfers_btn = tk.Button(self.btn_frame, text="Money Transfers", bg="#2b2b2b", fg="white", font=self.font2, command=self.create_money_transfer_widget, width=18)
        money_transfers_btn.grid(row=1, column=1, padx=2, pady=2)
        self.btn_frame.pack()

        self.exchange_frame = tk.Frame(self)
        exchange_btn = tk.Button(self.exchange_frame, text="Exchange", bg="#2b2b2b", fg="white", font=self.font2, command=self.create_exchange_widget, width=38)
        self.exchange_frame.pack()
        exchange_btn.pack()


    def create_account_info(self):
        account_info_background_path = "card_templates/AccountInfoBackground.png"
        account_info_background = Image.open(account_info_background_path)
        account_info_background = account_info_background.resize((333, 133), Image.LANCZOS)
        self.account_info_background = ImageTk.PhotoImage(account_info_background)

        self.canvas = tk.Canvas(self, width=333, height=133)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.account_info_background)

        self.canvas.create_text(162, 31, text=f"Account Type: {self.account.account_type}", fill="white", font=self.font1)
        self.canvas.create_text(162, 67, text=f"Account Number: {self.account.account_number}", fill="white", font=self.font1)
        self.canvas.create_text(162, 101, text=f"Balance: {self.account.balance} {self.account.currency}", fill="white", font=self.font1)

        self.canvas.pack(padx=10, pady=10)

    def create_payment_widget(self):
        PaymentWidget(self, Account.reload_account(self.account.account_id, self.account.currency))

    def create_bill_widget(self):
        BillWidget(self, Account.reload_account(self.account.account_id, self.account.currency))

    def create_saving_widget(self):
        SavingWidget(self, Account.reload_account(self.account.account_id, self.account.currency))

    def create_money_transfer_widget(self):
        MoneyTransferWidget(self, Account.reload_account(self.account.account_id, self.account.currency))
    
    def create_exchange_widget(self):
        ExchangeWidget(self, Account.reload_account(self.account.account_id, self.account.currency))

    def reload(self):
        self.parent.reload_widgets()
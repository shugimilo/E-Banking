import tkinter as tk
from utils.fetcher import Fetcher
from classes.account import Account
from classes.exchangerate import ExchangeRate
from tkinter import ttk
from tkinter.font import Font
from typing import List
from tkinter import messagebox

class ExchangeWidget(tk.Toplevel):
    def __init__(self, parent, account:Account):
        super().__init__(parent)
        self.parent = parent
        self.title("Exchange")
        self.geometry("850x300")
        self.account:Account = account
        self.font1 = Font(family="Courier New", size=12, weight="bold")
        self.font2 = Font(family="Courier New", size=12)
        self.currency_exchange_rates = []
        self.assign_currency_exchange_rates()
        self.currencies: List[ExchangeRate] = []
        for exchange_rate in self.currency_exchange_rates:
            self.currencies.append(exchange_rate.currency)

        self.main_frame = tk.Frame(self)
        self.main_frame.pack()

        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=1)

        self.rates_frame = ttk.Frame(self.notebook)

        rate_headers = ["Currency", "Buying Rate", "Mean Rate", "Selling Rate"]
        for column, header in enumerate(rate_headers):
            tk.Label(self.rates_frame, text=header, font=self.font1).grid(row=0, column=column, padx=10, pady=5)

        for row, currency in enumerate(self.currency_exchange_rates, start=1):
            tk.Label(self.rates_frame, text=f"{currency.currency}", font=self.font2).grid(row=row, column=0, padx=10, pady=5)
            tk.Label(self.rates_frame, text=f"{currency.buying_rate}", font=self.font2).grid(row=row, column=1, padx=10, pady=5)
            tk.Label(self.rates_frame, text=f"{currency.mean_rate}", font=self.font2).grid(row=row, column=2, padx=10, pady=5)
            tk.Label(self.rates_frame, text=f"{currency.selling_rate}", font=self.font2).grid(row=row, column=3, padx=10, pady=5)

        self.notebook.add(self.rates_frame, text="Currencies")

        self.exchange_frame = ttk.Frame(self.notebook)

        self.label_frame = tk.Frame(self.exchange_frame)
        self.label_frame.pack()

        warning_label = tk.Label(self.label_frame, text="Warning: You can only buy/sell \nthe foreign currencies \nwhich are associated \nto your foreign accounts.", font=self.font1)
        warning_label.pack(padx=10, pady=10)

        self.exchange_dialog_frame = tk.Frame(self.exchange_frame)
        self.exchange_dialog_frame.pack()
        if self.account.currency == "RSD":
            disclaimer_label = tk.Label(self.label_frame, text="Please enter currency codes using uppercase letters.\nExample: EUR, USD, GBP...", font=self.font1)
            disclaimer_label.pack(padx=10, pady=10)

            currency_label = tk.Label(self.exchange_dialog_frame, text="Currency", font=self.font1)
            currency_label.grid(row=0, column=0, padx=10, pady=5)
            self.currency_entry = tk.Entry(self.exchange_dialog_frame)
            self.currency_entry.grid(row=1, column=0, pady=5)
            amount_to_buy_label = tk.Label(self.exchange_dialog_frame, text="Amount to buy", font=self.font1)
            amount_to_buy_label.grid(row=0, column=1, padx=10, pady=5)
            self.amount_to_buy_entry = tk.Entry(self.exchange_dialog_frame)
            self.amount_to_buy_entry.grid(row=1, column=1, pady=5)
            fee_label = tk.Label(self.exchange_dialog_frame, text="Fee", font=self.font1)
            fee_label.grid(row=0, column=2, padx=10, pady=5)
            self.fee_display = tk.Label(self.exchange_dialog_frame, text=f"0 RSD", font=self.font2)
            self.fee_display.grid(row=1, column=2)
            amount_to_subtract_label = tk.Label(self.exchange_dialog_frame, text="Amount in RSD", font=self.font1)
            amount_to_subtract_label.grid(row=0, column=3)
            self.amount_to_subtract_display = tk.Label(self.exchange_dialog_frame, text=f"0 RSD", font=self.font2)
            self.amount_to_subtract_display.grid(row=1, column=3)

            calculate_btn = tk.Button(self.exchange_dialog_frame, text="Calculate", font=self.font2, command=self.calculate_fee_from_rsd_to_foreign)
            calculate_btn.grid(row=1, column=4, padx=5, pady=5)
            
            confirm_btn = tk.Button(self.exchange_dialog_frame, text="Confirm", font=self.font2, command=self.confirm_exchange_rsd_to_foreign)
            confirm_btn.grid(row=1, column=5, padx=5, pady=5)

            cancel_btn = tk.Button(self.exchange_dialog_frame, text="Cancel", font=self.font2, command=self.destroy)
            cancel_btn.grid(row=1, column=6, padx=5, pady=5)
        else:
            currency_label = tk.Label(self.exchange_dialog_frame, text="Currency", font=self.font1)
            currency_label.grid(row=0, column=0, padx=10, pady=5)
            foreign_currency_label = tk.Label(self.exchange_dialog_frame, text=f"{self.account.currency}", font=self.font2)
            foreign_currency_label.grid(row=1, column=0, padx=10, pady=5)
            amount_to_sell_label = tk.Label(self.exchange_dialog_frame, text="Amount to sell", font=self.font1)
            amount_to_sell_label.grid(row=0, column=1, padx=10, pady=5)
            self.amount_to_sell_entry = tk.Entry(self.exchange_dialog_frame)
            self.amount_to_sell_entry.grid(row=1, column=1, pady=5)
            fee_label = tk.Label(self.exchange_dialog_frame, text="Fee", font=self.font1)
            fee_label.grid(row=0, column=2, padx=10, pady=5)
            self.fee_display = tk.Label(self.exchange_dialog_frame, text=f"0 RSD", font=self.font2)
            self.fee_display.grid(row=1, column=2)
            amount_to_add_label = tk.Label(self.exchange_dialog_frame, text="Amount in RSD", font=self.font1)
            amount_to_add_label.grid(row=0, column=3)
            self.amount_to_add_display = tk.Label(self.exchange_dialog_frame, text=f"0 RSD", font=self.font2)
            self.amount_to_add_display.grid(row=1, column=3)

            calculate_btn = tk.Button(self.exchange_dialog_frame, text="Calculate", font=self.font2, command=self.calculate_fee_from_foreign_to_rsd)
            calculate_btn.grid(row=1, column=4, padx=5, pady=5)
            
            confirm_btn = tk.Button(self.exchange_dialog_frame, text="Confirm", font=self.font2, command=self.confirm_exchange_foreign_to_rsd)
            confirm_btn.grid(row=1, column=5, padx=5, pady=5)

            cancel_btn = tk.Button(self.exchange_dialog_frame, text="Cancel", font=self.font2, command=self.destroy)
            cancel_btn.grid(row=1, column=6, padx=5, pady=5)

        self.notebook.add(self.exchange_frame, text="Exchange")

        self.transactions_frame = ttk.Frame(self.notebook)
        transaction_headers = ["From amount", "To amount", "Rate", "Fee", "Date"]
        for column, header in enumerate(transaction_headers):
            tk.Label(self.transactions_frame, text=header, font=self.font1).grid(row=0, column=column, padx=10, pady=5)
        
        for row, transaction in enumerate(self.account.exchange_transactions, start=1):
            tk.Label(self.transactions_frame, text=f"{transaction.from_amount}{transaction.from_currency}", font=self.font2).grid(row=row, column=0, padx=10, pady=5)
            tk.Label(self.transactions_frame, text=f"{transaction.to_amount}{transaction.to_currency}", font=self.font2).grid(row=row, column=1, padx=10, pady=5)
            tk.Label(self.transactions_frame, text=f"{transaction.exchange_rate}", font=self.font2).grid(row=row, column=2, padx=10, pady=5)
            tk.Label(self.transactions_frame, text=f"{transaction.fee}", font=self.font2).grid(row=row, column=3, padx=10, pady=5)
            tk.Label(self.transactions_frame, text=f"{transaction.transaction_date}", font=self.font2).grid(row=row, column=4, padx=10, pady=5)

        self.notebook.add(self.transactions_frame, text="Past Exchanges")

    def calculate_fee_from_rsd_to_foreign(self):
        if self.currency_entry.get():
            if self.currency_entry.get() in self.currencies:
                currency = self.currency_entry.get()
                fetcher = Fetcher()
                if fetcher.checkIfUserHasForeignAccount(self.account.user_id, currency):
                    if self.amount_to_buy_entry.get():
                        if float(self.amount_to_buy_entry.get()) > self.account.balance:
                            messagebox.showinfo(title="Error", message="Amount exceeds your balance.")
                        else:
                            amount_to_buy = float(self.amount_to_buy_entry.get())
                            for exchange_rate in self.currency_exchange_rates:
                                if exchange_rate.currency == currency:
                                    self.amount_to_subtract, self.fee, rate = exchange_rate.rsd_to_foreign(amount_to_buy)
                                    self.fee_display.destroy()
                                    self.fee_display = tk.Label(self.exchange_dialog_frame, text=f"{self.fee} RSD", font=self.font2)
                                    self.fee_display.grid(row=1, column=2)
                                    self.amount_to_subtract_display.destroy()
                                    self.amount_to_subtract_display = tk.Label(self.exchange_dialog_frame, text=f"{self.amount_to_subtract} RSD")
                                    self.amount_to_subtract_display.grid(row=1, column=3)
                                    return currency, amount_to_buy
                    else:
                        messagebox.showinfo(title="Error", message="Please enter an amount.")
                        return 0, 0
                else:
                    messagebox.showinfo(title="Error", message=f"You do not have an account associated with this currency ({currency}).")
                    return 0, 0
            else:
                messagebox.showinfo(title="Error", message="Please select a foreign currency that exists in the system.")
                return 0, 0
        else:
            messagebox.showinfo(title="Error", message="Please choose a currency")
            return 0, 0
        
    def calculate_fee_from_foreign_to_rsd(self):
        if self.amount_to_sell_entry.get():
            amount_to_sell = float(self.amount_to_sell_entry.get())
            if amount_to_sell >= self.account.balance:
                messagebox.showinfo(title="Error", message="Amount exceeds your account balance.")
                return 0
            else:
                for exchange_rate in self.currency_exchange_rates:
                    if exchange_rate.currency == self.account.currency:
                        self.amount_to_add, self.fee, buying_rate = exchange_rate.foreign_to_rsd(amount_to_sell)
                        self.fee_display.destroy()
                        self.fee_display.destroy()
                        self.fee_display = tk.Label(self.exchange_dialog_frame, text=f"{self.fee} RSD", font=self.font2)
                        self.fee_display.grid(row=1, column=2)
                        self.amount_to_add_display.destroy()
                        self.amount_to_add_display = tk.Label(self.exchange_dialog_frame, text=f"{self.amount_to_add} RSD")
                        self.amount_to_add_display.grid(row=1, column=3)  
                        return amount_to_sell
        else:
            messagebox.showinfo(title="Error", message="Please enter an amount.")
            return 0


    def confirm_exchange_rsd_to_foreign(self):
        currency, amount_to_buy = self.calculate_fee_from_rsd_to_foreign()
        if (currency != 0) & (amount_to_buy != 0):
            other_account = Account.fetch_foreign_account(self.account.user_id, currency)
            if(self.account.buy_foreign_currency(other_account, amount_to_buy)):
                messagebox.showinfo(title="Success", message="Exchange successful.")
                self.parent.reload()
                self.destroy()

    def confirm_exchange_foreign_to_rsd(self):
        amount_to_sell = self.calculate_fee_from_foreign_to_rsd()
        if amount_to_sell != 0:
            other_account = Account.fetch_foreign_account(self.account.user_id, "RSD")
            if self.account.sell_foreign_currency(other_account, amount_to_sell):
                messagebox.showinfo(title="Success", message="Exchange successful.")
                self.parent.reload()
                self.destroy()


    def assign_currency_exchange_rates(self):
        fetcher = Fetcher()
        currencies = fetcher.fetchAllCurrencies()
        for currency in currencies:
            self.currency_exchange_rates.append(ExchangeRate(currency["currency"]))
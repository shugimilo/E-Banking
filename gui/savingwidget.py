import tkinter as tk
from tkinter.font import Font
from classes.account import Account
from classes.saving import Saving
from utils.etcher import Etcher
from functools import partial
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import date

class SavingWidget(tk.Toplevel):
    def __init__(self, parent, account:Account):
        super().__init__(parent)
        self.parent = parent
        self.title("Savings")
        self.geometry("1200x400")
        self.account = account
        self.savings = account.savings
        self.font = Font(family="Courier New", size=12)

        self.main_frame = tk.Frame(self)
        self.main_frame.pack()

        self.process_savings()
        self.second_frame = tk.Frame(self)
        self.second_frame.pack()

        create_saving_btn = tk.Button(self.second_frame, text='Create New Saving', font=self.font, command=self.prompt_saving_creation)
        create_saving_btn.pack()

    def process_savings(self):
        headers = ["Goal Name", "Goal Amount", "Start Date", "End Date", "Saved Amount", "Percentage Saved", "Status", "Action"]
        for column, header in enumerate(headers):
            tk.Label(self.main_frame, text=header, font=("Courier New", 14, "bold")).grid(row=0, column=column, padx=5, pady=5)
        for row, saving in enumerate(self.savings, start=1):
            tk.Label(self.main_frame, text=f"{saving.goal_name}", font=self.font).grid(row=row, column=0, padx=5, pady=5)
            tk.Label(self.main_frame, text=f"{saving.goal_amount} {self.account.currency}", font=self.font).grid(row=row, column=1, padx=5, pady=5)
            tk.Label(self.main_frame, text=f"{saving.start_date}", font=self.font).grid(row=row, column=2, padx=5, pady=5)
            tk.Label(self.main_frame, text=f"{saving.end_date}", font=self.font).grid(row=row, column=3, padx=5, pady=5)
            tk.Label(self.main_frame, text=f"{saving.saved_amount} {self.account.currency}", font=self.font).grid(row=row, column=4, padx=5, pady=5)
            if (saving.status == "active"):
                tk.Label(self.main_frame, text=f"{round((saving.saved_amount / saving.goal_amount), 2) * 100}%", font=self.font).grid(row=row, column=5, padx=5, pady=5)
            else:
                tk.Label(self.main_frame, text="100%", font=self.font).grid(row=row, column=5, padx=5, pady=5)
            tk.Label(self.main_frame, text=f"{saving.status}", font=self.font).grid(row=row, column=6, padx=5, pady=5)
            if ((saving.status == "active") & (saving.saved_amount < saving.goal_amount)):
                tk.Button(self.main_frame, text="Add Funds", font=self.font, command=partial(self.add_to_saving, saving)).grid(row=row, column=7, padx=5, pady=5)
            elif((saving.saved_amount >= saving.goal_amount) & (saving.status == "active")):
                tk.Button(self.main_frame, text="Withdraw", font=self.font, command=partial(self.confirm_withdrawal, saving)).grid(row=row, column=7, padx=5, pady=5)
            else:
                tk.Label(self.main_frame, text="None", font=self.font).grid(row=row, column=7, padx=5, pady=5)

    def confirm_withdrawal(self, saving:Saving):
        self.withdrawal_popup = tk.Toplevel(self)
        self.withdrawal_popup.title("Confirm Withdrawal")
        self.withdrawal_popup.geometry("750x200")
        frame = tk.Frame(self.withdrawal_popup)
        frame.pack()
        label = tk.Label(frame, text=f"Are you sure that you want to withdraw {saving.saved_amount} {self.account.currency} from the saving '{saving.goal_name}'",font=self.font)
        label.pack()
        btn_frame = tk.Frame(self.withdrawal_popup)
        btn_frame.pack()
        yes_btn = tk.Button(btn_frame, text="Yes", font=self.font, command=partial(self.withdrawal_confirmed, saving))
        yes_btn.grid(row=0, column=0, padx=10, pady=10)
        no_btn = tk.Button(btn_frame, text="No", font=self.font, command=self.withdrawal_popup.destroy)
        no_btn.grid(row=0, column=1, padx=10, pady=10)

    def withdrawal_confirmed(self, saving:Saving):
        self.account.withdraw_from_saving(saving, saving.saved_amount)
        etcher = Etcher()
        etcher.closeSaving(saving.savings_id)
        self.parent.reload()
        self.withdrawal_popup.destroy()

    def add_to_saving(self, saving:Saving):
        self.addition_popup = tk.Toplevel(self)
        self.addition_popup.title("Add to saving")
        self.addition_popup.geometry("400x200")
        frame = tk.Frame(self.addition_popup)
        frame.pack()
        label = tk.Label(frame, text="Enter amount to add", font=self.font)
        label.grid(row=0, column=0, padx=10, pady=5)
        self.amount_entry = tk.Entry(frame)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)
        currency_label = tk.Label(frame, text=self.account.currency, font=self.font)
        currency_label.grid(row=0, column=2, pady=5)
        btn_frame = tk.Frame(self.addition_popup)
        btn_frame.pack()
        confirm_btn = tk.Button(btn_frame, text="Confirm", font=self.font, command=partial(self.confirm_addition_to_saving, saving))
        confirm_btn.grid(row=0, column=0, padx=10, pady=10)
        cancel_btn = tk.Button(btn_frame, text="Cancel", font=self.font, command=self.addition_popup.destroy)
        cancel_btn.grid(row=0, column=1, padx=10, pady=10)

    def confirm_addition_to_saving(self, saving:Saving):
        amount_string = self.amount_entry.get()
        amount = float(amount_string)
        if amount <= self.account.balance:
            if amount + saving.saved_amount > saving.goal_amount:
                overflow = saving.saved_amount + amount - saving.goal_amount
                amount -= overflow
            self.account.add_to_saving(saving, amount)
            messagebox.showinfo(title="Notification", message="Success.")
            self.parent.reload()
        else:
            messagebox.showinfo(title="Notification", message="You do not have enough funds for this action.")
            self.addition_popup.destroy()

    def prompt_saving_creation(self):
        self.creation_popup = tk.Toplevel(self)
        self.creation_popup.title("Create New Saving")
        self.creation_popup.geometry("600x200")
        frame = tk.Frame(self.creation_popup)
        frame.pack()
        tk.Label(frame, text="Goal Name", font=("Courier New", 12, "bold")).grid(row=0, column=0, padx=10, pady=5)
        self.goal_name_entry = tk.Entry(frame)
        self.goal_name_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(frame, text="Goal Amount", font=("Courier New", 12, "bold")).grid(row=1, column=0, padx=10, pady=5)
        self.goal_amount_entry = tk.Entry(frame)
        self.goal_amount_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(frame, text=self.account.currency, font=("Courier New", 12, "bold")).grid(row=1, column=2, pady=5)
        tk.Label(frame, text="Start Date", font=("Courier New", 12, "bold")).grid(row=2, column=0, padx=10, pady=5)
        self.start_date_entry = DateEntry(frame)
        self.start_date_entry.grid(row=2, column=1, padx=10, pady=5)
        tk.Label(frame, text="End Date", font=("Courier New", 12, "bold")).grid(row=3, column=0, padx=10, pady=5)
        self.end_date_entry = DateEntry(frame)
        self.end_date_entry.grid(row=3, column=1, padx=10, pady=5)

        btn_frame = tk.Frame(self.creation_popup)
        btn_frame.pack()
        confirm_btn = tk.Button(btn_frame, text="Confirm", font=self.font, command=self.confirm_saving_addition)
        confirm_btn.grid(row=0, column=0, padx=10, pady=5)
        cancel_btn = tk.Button(btn_frame, text="Cancel", font=self.font, command=self.creation_popup.destroy)
        cancel_btn.grid(row=0, column=1, padx=10, pady=5)
    
    def confirm_saving_addition(self):
        goal_name = self.goal_name_entry.get()
        goal_amount_str = self.goal_amount_entry.get()
        error_messages = []
        if goal_amount_str != '':
            goal_amount = float(goal_amount_str)
        else:
            goal_amount = 0
            error_messages.append("Cannot leave goal amount field empty.")
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()
        if len(goal_name) > 255:
            error_messages.append("Goal name too long (over 255 characters).")
        if goal_amount <= 0:
            error_messages.append("Goal amount must be a positive number.")
        if start_date < date.today():
            error_messages.append("Start day cannot be in the past.")
        if end_date < date.today():
            error_messages.append("End date cannot be in the past.")
        if end_date < start_date:
            error_messages.append("End date cannot be before start date chronologically.")
        if len(error_messages) > 0:
            error_message = ""
            for message in error_messages:
                error_message += message + "\n"
            messagebox.showinfo(title="Error", message=f"{error_message}")
        else:
            self.account.create_saving(goal_amount, goal_name, start_date, end_date)
            self.parent.reload()
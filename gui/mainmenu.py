import tkinter as tk
from .app import App
from .accountwidget import AccountWidget, Account
from typing import List
from tkinter.font import Font

class MainMenu(tk.Frame):
    def __init__(self, app:App):
        super().__init__(app)
        self.root:App = app
        self.root.set_geometry(500, 600)
        self.pack()
        self.font = Font(family="Courier New", size=14, weight="bold")
        self.create_widgets(app)

    def create_widgets(self, app):
        welcome = f"Welcome, {app.user.first_name} {app.user.last_name}!"
        self.label = tk.Label(self, text=welcome, font=("Courier New", 16, "bold"))
        self.label.pack(pady=10)

        self.label2 = tk.Label(self, text="Here are your accounts", font=self.font)
        self.label2.pack(pady=10)

        self.accounts: List[Account] = []
        for account in app.user.accounts:
                self.accounts.append(account)
        self.current_account_index = 0

        self.left_button = tk.Button(self, text="<", command=self.show_prev_account, font=self.font, bg="#2b2b2b", fg="white")
        self.left_button.pack(side=tk.LEFT, padx=10)

        self.right_button = tk.Button(self, text=">", command=self.show_next_account, font=self.font, bg="#2b2b2b", fg="white")
        self.right_button.pack(side=tk.RIGHT, padx=10)

        self.account_frame = tk.Frame(self)
        self.account_frame.pack()

        self.account_widget = AccountWidget(self.account_frame, self, self.accounts[self.current_account_index])
        self.account_widget.pack()

    def show_prev_account(self):
        self.current_account_index = (self.current_account_index - 1) % len(self.accounts)
        self.update_account()

    def show_next_account(self):
        self.current_account_index = (self.current_account_index + 1) % len(self.accounts)
        self.update_account()

    def update_account(self):
        for widget in self.account_frame.winfo_children():
            widget.destroy()
        self.account_widget = AccountWidget(self.account_frame, self, self.accounts[self.current_account_index])
        self.account_widget.pack()

    def reload_widgets(self):
        self.root.reload_user_accounts()
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets(self.root)
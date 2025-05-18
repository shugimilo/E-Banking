import tkinter as tk
from tkinter import messagebox
from utils.fetcher import Fetcher
from gui.app import App
from classes.user import User
from gui.mainmenu import MainMenu
from tkinter.font import Font

class SignIn(tk.Frame):
    def __init__(self, app: App):
        super().__init__(app)
        self.root:App = app
        self.root.set_geometry(300, 200)
        self.pack()
        self.font:Font = Font(family="Courier New", size=12)

        self.label = tk.Label(self, text="Sign In", font=("Courier New", 16))
        self.label.pack(padx=10, pady=10)
        
        entry_frame = tk.Frame(self)
        entry_frame.pack()
        username_label = tk.Label(entry_frame, text="Username:", font=self.font).grid(row=0, column=0, padx=5, pady=5)
        pwd_label = tk.Label(entry_frame, text="Password: ", font=self.font).grid(row=1, column=0, padx=5, pady=5)
        self.username_box = tk.Entry(entry_frame)
        self.pwd_box = tk.Entry(entry_frame, show="*")
        self.username_box.grid(row=0, column=1, padx=5, pady=5)
        self.pwd_box.grid(row=1, column=1, padx=10, pady=5)

        self.sign_in_button = tk.Button(self, text="Go", command=self.sign_in)
        self.sign_in_button.pack(pady=10)

    def sign_in(self):
        fetcher = Fetcher()
        if (self.username_box.get()):
            username = self.username_box.get().strip()
            result = fetcher.fetchUserPwd(username)[0]
            if result:
                pwd = self.pwd_box.get().strip()
                if pwd == result['pwd']:
                    user = User(username, pwd)
                    self.root.set_user(user)
                    self.destroy()
                    self.root.switch_frame(MainMenu)
                else:
                    messagebox.showerror(title="Error", message="Incorrect password.")
            else:
                messagebox.showerror(title="Error", message="Username not found.")
        else:
            messagebox.showerror(title="Error", message="Please enter your credentials.")

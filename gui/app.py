import tkinter as tk
from classes.user import User
from utils.fetcher import Fetcher

class App(tk.Tk):
    user = User

    def __init__(self):
        super().__init__()
        self.title("Online Banking App")
        self.geometry("600x600")
        self.minsize(400, 400)

    def switch_frame(self, frame_class, *args):
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()
        self.current_frame = frame_class(self, *args)
        self.current_frame.pack()

    def set_user(self, user):
        App.user = user

    def reload_user_accounts(self):
        fetcher = Fetcher()
        refreshed_accounts = fetcher.fetchUserAccounts(App.user.id)
        App.user.accounts = []
        App.user.assign_accounts(refreshed_accounts)

    def set_geometry(self, width, height):
        self.geometry(f"{width}x{height}")
        self.minsize(width, height)
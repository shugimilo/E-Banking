import tkinter as tk
from tkinter.font import Font
from PIL import Image, ImageTk
from classes.creditcard import CreditCard
from datetime import date

class CardWidget(tk.Frame):
    def __init__(self, parent, card:CreditCard):
        super().__init__(parent)
        self.parent = parent
        self.card:CreditCard = card
        self.font = Font(family="Courier New", size=14, weight="bold")
        self.create_card_image()

    def create_card_image(self):
        path = "card_templates/"
        full_path = path + self.card.card_type + ".png"
        card_image = Image.open(full_path)
        card_image = card_image.resize((333, 221), Image.LANCZOS)
        self.card_image_tk = ImageTk.PhotoImage(card_image)

        self.canvas = tk.Canvas(self, width=333, height=221)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.card_image_tk)

        card_quartets = CardWidget.split_string_after_n_chars(self.card.card_number, 4)
        new_card_number = ''
        for quartet in card_quartets:
            new_card_number += quartet + " "
        new_name = self.card.cardholder_name.upper()
        new_date = CardWidget.convert_date_format(self.card.expiration_date)
        self.canvas.create_text(125, 167, text=new_card_number, fill="white", font=self.font)
        self.canvas.create_text(242, 32, text=new_name, fill="white", font=self.font)
        self.canvas.create_text(242, 64, text=new_date, fill="white", font=self.font)

        self.canvas.pack()
    
    @staticmethod
    def split_string_after_n_chars(string, n):
        return [string[i:i+n] for i in range(0, len(string), n)]
    
    @staticmethod
    def convert_date_format(date_obj):
        if isinstance(date_obj, date):
            formatted_date = date_obj.strftime('%m/%y')
            return formatted_date
        else:
            raise ValueError("Input must be a datetime.date object.")

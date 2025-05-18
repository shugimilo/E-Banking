class CreditCard:
    def __init__(self, card_id, account_id, card_type, card_number, cardholder_name, expiration_date, cvv, status):
        self.card_id = card_id
        self.account_id = account_id
        self.card_type = card_type
        self.card_number = card_number
        self.cardholder_name = cardholder_name
        self.expiration_date = expiration_date
        self.cvv = cvv
        self.status = status
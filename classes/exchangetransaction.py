class ExchangeTransaction:
    def __init__(self, transaction_id, user_id, from_account_id, to_account_id, from_amount, to_amount, exchange_rate, fee, transaction_date, from_currency, to_currency):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.from_account_id = from_account_id
        self.to_account_id = to_account_id
        self.from_amount = round(float(from_amount), 2)
        self.to_amount = round(float(to_amount), 2)
        self.exchange_rate = round(float(exchange_rate), 2)
        self.fee = round(float(fee), 2)
        self.transaction_date = transaction_date.date()
        self.from_currency = from_currency
        self.to_currency = to_currency
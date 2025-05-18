class Payment:
    def __init__(self, payment_id, account_id, amount_paid, paid_to, payment_date):
        self.payment_id = payment_id
        self.account_id = account_id
        self.amount_paid = amount_paid
        self.paid_to = paid_to
        self.payment_date = payment_date.date()
class BillPayment:
    def __init__(self, payment_id, bill_id, account_id, amount_paid, payment_date, biller_name):
        self.payment_id = payment_id
        self.bill_id = bill_id
        self.account_id = account_id
        self.amount_paid = amount_paid
        self.payment_date = payment_date.date()
        self.biller_name = biller_name
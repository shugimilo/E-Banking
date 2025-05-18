class Bill:
    def __init__(self, bill_id, account_id, biller_name, bill_amount, due_date, status, payment_date):
        self.bill_id = bill_id
        self.account_id = account_id
        self.biller_name = biller_name
        self.bill_amount = float(bill_amount)
        self.due_date = due_date
        self.status = status
        self.payment_date = payment_date
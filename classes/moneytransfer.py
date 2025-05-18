class MoneyTransfer:
    def __init__(self, transfer_id, sender_account_id, receiver_account_id, amount, transfer_date, recipient_name, recipient_address, recipient_city, payment_code, model, reference_number, payment_purpose):
        self.transfer_id = transfer_id
        self.sender_account_id = sender_account_id
        self.receiver_account_id = receiver_account_id
        self.amount = amount
        self.transfer_date = transfer_date.date()
        self.recipient_name = recipient_name
        self.recipient_address = recipient_address
        self.recipient_city = recipient_city
        self.payment_code = payment_code
        self.model = model
        self.reference_number = reference_number
        self.payment_purpose = payment_purpose
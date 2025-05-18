from utils.database import Database
from datetime import datetime

class Etcher:
    def __init__(self):
        self.connection = Database()

    def uploadBillPayment(self, bill_id, account_id, bill_amount, biller_name):
        query = "INSERT INTO bill_payments(bill_id, account_id, amount_paid, payment_date, biller_name) VALUES (%s, %s, %s, %s, %s);"
        current_time = datetime.now()
        formatted_current_time = current_time.strftime('%Y-%m-%d %H-%M-%S')
        self.connection.execute(query, (bill_id, account_id, bill_amount, formatted_current_time, biller_name))

    def updateBill(self, bill_id):
        query = "UPDATE bills SET status = 'paid', payment_date = %s WHERE bill_id = %s;"
        current_time = datetime.now()
        formatted_current_time = current_time.strftime('%Y-%m-%d')
        self.connection.execute(query, (formatted_current_time, bill_id))

    def updateBalance(self, account_id, new_balance):
        query = "UPDATE accounts SET balance = %s WHERE account_id = %s;"
        self.connection.execute(query, (new_balance, account_id))

    def uploadExchangeTransaction(self, user_id, from_account_id, to_account_id, from_amount, to_amount, exchange_rate, fee, from_currency, to_currency):
        query = "INSERT INTO exchange_transactions(user_id, from_account_id, to_account_id, from_amount, to_amount, exchange_rate, fee, from_currency, to_currency) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        self.connection.execute(query, (user_id, from_account_id, to_account_id, from_amount, to_amount, exchange_rate, fee, from_currency, to_currency))

    def uploadMoneyTransfer(self, sender_account_id, receiver_account_id, amount, recipient_name, recipient_address, recipient_city, payment_code, model, reference_number, payment_purpose):
        query = "INSERT INTO money_transfers(sender_account_id, receiver_account_id, amount, recipient_name, recipient_address, recipient_city, payment_code, model, reference_number, payment_purpose) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        self.connection.execute(query, (sender_account_id, receiver_account_id, amount, recipient_name, recipient_address, recipient_city, payment_code, model, reference_number, payment_purpose))

    def uploadSaving(self, user_id, account_id, goal_amount, goal_name, start_date, end_date, saved_amount):
        query = "INSERT INTO savings(user_id, account_id, goal_amount, goal_name, start_date, end_date, saved_amount, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        self.connection.execute(query, (user_id, account_id, goal_amount, goal_name, start_date, end_date, saved_amount, "active"))

    def updateSaving(self, saving_id, new_amount):
        query = "UPDATE savings SET saved_amount = %s WHERE savings_id = %s;"
        self.connection.execute(query, (new_amount, saving_id))

    def closeSaving(self, saving_id):
        query = "UPDATE savings SET status = 'completed', saved_amount = goal_amount WHERE savings_id = %s;"
        self.connection.execute(query, (saving_id, ))
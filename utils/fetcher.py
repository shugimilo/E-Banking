from utils.database import Database

class Fetcher:
    def __init__(self):
        self.connection = Database()

    def fetchUserPwd(self, username):
        query = "SELECT pwd FROM users u WHERE u.username = %s;"
        results = self.connection.query(query, (username, ))
        return results

    def fetchUserAccounts(self, user_id):
        query = 'SELECT DISTINCT a.account_id, a.user_id, a.account_number, a.account_type, a.balance, a.currency FROM accounts a WHERE a.user_id = %s;'
        results = self.connection.query(query, (user_id, ))
        return results
    
    def fetchAccountCards(self, account_id):
        query = "SELECT DISTINCT c.card_id, c.account_id, c.card_type, c.card_number, c.cardholder_name, c.expiration_date, c.cvv, c.status FROM credit_cards c WHERE c.account_id = %s;"
        results = self.connection.query(query, (account_id, ))
        return results
    
    def fetchAccountBills(self, account_id):
        query = "SELECT DISTINCT b.bill_id, b.account_id, b.biller_name, b.bill_amount, b.due_date, b.status, b.payment_date FROM bills b WHERE b.account_id = %s;"
        results = self.connection.query(query, (account_id, ))
        return results

    def fetchAccountBillPayments(self, account_id):
        query = "SELECT DISTINCT p.payment_id, p.bill_id, p.account_id, p.amount_paid, p.payment_date, p.biller_name FROM bill_payments p WHERE p.account_id = %s;"
        results = self.connection.query(query, (account_id, ))
        return results
    
    def fetchAccountSavings(self, account_id):
        query = "SELECT DISTINCT s.savings_id, s.user_id, s.account_id, s.goal_amount, s.goal_name, s.start_date, s.end_date, s.saved_amount, s.status FROM savings s WHERE s.account_id = %s;"
        results = self.connection.query(query, (account_id, ))
        return results
    
    def fetchAccountMoneyTransfers(self, account_id):
        query = "SELECT DISTINCT m.transfer_id, m.sender_account_id, m.receiver_account_id, m.amount, m.transfer_date, m.recipient_name, m.recipient_address, m.recipient_city, m.payment_code, m.model, m.reference_number, m.payment_purpose FROM money_transfers m WHERE m.sender_account_id = %s OR m.receiver_account_id = %s;"
        results = self.connection.query(query, (account_id, account_id))
        return results
    
    def fetchAccountExchangeTransactions(self, account_id):
        query = "SELECT DISTINCT t.transaction_id, t.user_id, t.from_account_id, t.to_account_id, t.from_amount, t.to_amount, t.exchange_rate, t.fee, t.transaction_date, t.from_currency, t.to_currency FROM exchange_transactions t WHERE t.from_account_id = %s OR t.to_account_id = %s;"
        results = self.connection.query(query, (account_id, account_id))
        return results
    
    def fetchUserAccountByFullName(self, full_name:str, currency:str):
        query = "SELECT DISTINCT a.account_id, a.user_id, a.account_number, a.account_type, a.balance, a.currency FROM accounts a JOIN users u ON a.user_id = u.id WHERE concat(u.first_name, ' ', u.last_name) = %s AND a.currency = %s;"
        results = self.connection.query(query, (full_name, currency))
        return results
    
    def fetchUserAccountByID(self, id:str, currency:str):
        query = "SELECT DISTINCT a.account_id, a.user_id, a.account_number, a.account_type, a.balance, a.currency FROM accounts a WHERE a.user_id = %s AND a.currency = %s;"
        results = self.connection.query(query, (id, currency))
        return results
    
    def reloadAccount(self, account_id, currency):
        query = "SELECT DISTINCT a.account_id, a.user_id, a.account_number, a.account_type, a.balance, a.currency FROM accounts a WHERE a.account_id = %s AND a.currency = %s;"
        results = self.connection.query(query, (account_id, currency))
        return results
    
    def fetchAccountPayments(self, account_id):
        query = "SELECT DISTINCT p.payment_id, p.account_id, p.amount_paid, p.paid_to, p.payment_date FROM payments p WHERE p.account_id = %s;"
        results = self.connection.query(query, (account_id, ))
        return results
    
    def fetchUserInfoByAccountID(self, account_id):
        query = "SELECT DISTINCT u.first_name, u.last_name FROM users u JOIN accounts a ON u.id = a.user_id WHERE a.account_id = %s;"
        results = self.connection.query(query, (account_id, ))
        return results[0]
    
    def checkIfUserExists(self, full_name):
        query = "SELECT DISTINCT a.account_id, a.user_id, a.account_number, a.account_type, a.balance, a.currency FROM accounts a JOIN users u ON a.user_id = u.id WHERE concat(u.first_name, ' ', u.last_name) = %s;"
        results = self.connection.query(query, (full_name, ))
        if len(results) > 0:
            return 1
        else:
            return 0
        
    def checkIfUserHasForeignAccount(self, user_id, foreign_currency):
        query = "SELECT DISTINCT account_id FROM accounts WHERE user_id = %s AND currency = %s;"
        results = self.connection.query(query, (user_id, foreign_currency))
        if len(results) > 0:
            return 1
        else:
            return 0
        
    def fetchAllCurrencies(self):
        query = "SELECT DISTINCT currency FROM exchange_rates;"
        results = self.connection.query(query, ())
        return results

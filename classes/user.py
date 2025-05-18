from utils.database import Database
from utils.fetcher import Fetcher
from .account import Account
from typing import List, Dict

class User:
    def __init__(self, username, pwd):
        db = Database()
        fetcher = Fetcher()
        query = "SELECT * FROM users WHERE username = %s AND pwd = %s;"
        fetched_users = db.query(query, (username, pwd))

        if fetched_users:
            fetched_user = fetched_users[0]
            if (fetched_user['username'] == username) & (fetched_user['pwd'] == pwd):
                self.id = fetched_user['id']
                self.username = fetched_user['username']
                self.pwd = fetched_user['pwd']
                self.first_name = fetched_user['first_name']
                self.last_name = fetched_user['last_name']
                self.email = fetched_user['email']
                self.date_of_birth = fetched_user['date_of_birth']
                self.accounts: List[Account] = []

                accounts = fetcher.fetchUserAccounts(self.id)
                self.assign_accounts(accounts)
            else:
                raise ValueError('Wrong user credentials.\n')
        else:
            raise ValueError("User doesn't exist.\n")
        
    def assign_account(self, fa:Dict[str, any]):
        return Account(fa['account_id'], fa['user_id'], fa['account_number'], fa['account_type'], fa['balance'], fa['currency'])
    
    def assign_accounts(self, fas:List[Dict[str, any]]):
        for fa in fas:
            self.accounts.append(self.assign_account(fa))
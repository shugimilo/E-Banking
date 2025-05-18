from .creditcard import CreditCard
from .bill import Bill
from .billpayment import BillPayment
from .saving import Saving
from .moneytransfer import MoneyTransfer
from .exchangetransaction import ExchangeTransaction
from .exchangerate import ExchangeRate
from .payment import Payment
from typing import List, Dict
from utils.fetcher import Fetcher
from utils.etcher import Etcher
from datetime import datetime

class Account:
    def __init__(self, account_id, user_id, account_number, account_type, balance, currency):
        fetcher = Fetcher()

        self.account_id = account_id
        self.user_id = user_id
        self.account_number = account_number
        self.account_type = account_type
        self.balance = float(balance)
        self.currency = currency
        self.cards: List[CreditCard] = []
        self.bills: List[Bill] = []
        self.bill_payments: List[BillPayment] = []
        self.savings: List[Saving] = []
        self.money_transfers: List[MoneyTransfer] = []
        self.exchange_transactions: List[ExchangeTransaction] = []
        self.payments: List[Payment] = []
        
        self.assign_cards(fetcher.fetchAccountCards(self.account_id))
        self.assign_bills(fetcher.fetchAccountBills(self.account_id))
        self.assign_bill_payments(fetcher.fetchAccountBillPayments(self.account_id))
        self.assign_savings(fetcher.fetchAccountSavings(self.account_id))
        self.assign_money_transfers(fetcher.fetchAccountMoneyTransfers(self.account_id))
        self.assign_exchange_transactions(fetcher.fetchAccountExchangeTransactions(self.account_id))
        self.assign_payments(fetcher.fetchAccountPayments(self.account_id))

    @staticmethod
    def fetch_other_account(recipient_name, currency):
        fetcher = Fetcher()
        results = fetcher.fetchUserAccountByFullName(recipient_name, currency)
        result = results[0]
        account_id = result['account_id']
        user_id = result['user_id']
        account_number = result['account_number']
        account_type = result['account_type']
        balance = result['balance']
        currency = result['currency']
        return Account(account_id, user_id, account_number, account_type, balance, currency)
    
    @staticmethod
    def fetch_foreign_account(user_id, currency):
        fetcher = Fetcher()
        results = fetcher.fetchUserAccountByID(user_id, currency)
        result = results[0]
        account_id = result['account_id']
        user_id = result['user_id']
        account_number = result['account_number']
        account_type = result['account_type']
        balance = result['balance']
        currency = result['currency']
        return Account(account_id, user_id, account_number, account_type, balance, currency)

    @staticmethod
    def reload_account(account_id, currency):
        fetcher = Fetcher()
        results = fetcher.reloadAccount(account_id, currency)
        result = results[0]
        account_id = result['account_id']
        user_id = result['user_id']
        account_number = result['account_number']
        account_type = result['account_type']
        balance = result['balance']
        currency = result['currency']
        return Account(account_id, user_id, account_number, account_type, balance, currency)
    
    def assign_card(self, fc:Dict[str, any]):
        return CreditCard(fc['card_id'], fc['account_id'], fc['card_type'], fc['card_number'], fc['cardholder_name'], fc['expiration_date'], fc['cvv'], fc['status'])
    
    def assign_cards(self, fcs:List[Dict[str, any]]):
        for fc in fcs:
            self.cards.append(self.assign_card(fc))

    def assign_bill(self, fb:Dict[str, any]):
        return Bill(fb['bill_id'], fb['account_id'], fb['biller_name'], fb['bill_amount'], fb['due_date'], fb['status'], fb['payment_date'])
    
    def assign_bills(self, fbs:List[Dict[str, any]]):
        for fb in fbs:
            self.bills.append(self.assign_bill(fb))

    def assign_bill_payment(self, fbp:Dict[str, any]):
        return BillPayment(fbp['payment_id'], fbp['bill_id'], fbp['account_id'], fbp['amount_paid'], fbp['payment_date'], fbp['biller_name'])
    
    def assign_bill_payments(self, fbps:List[Dict[str, any]]):
        for fbp in fbps:
            self.bill_payments.append(self.assign_bill_payment(fbp))

    def assign_saving(self, fs:Dict[str, any]):
        return Saving(fs['savings_id'], fs['user_id'], fs['account_id'], fs['goal_amount'], fs['goal_name'], fs['start_date'], fs['end_date'], fs['saved_amount'], fs['status'])
    
    def assign_savings(self, fss:List[Dict[str, any]]):
        for fs in fss:
            self.savings.append(self.assign_saving(fs))

    def assign_money_transfer(self, fmt:Dict[str, any]):
        return MoneyTransfer(fmt['transfer_id'], fmt['sender_account_id'], fmt['receiver_account_id'], fmt['amount'], fmt['transfer_date'], fmt['recipient_name'], fmt['recipient_address'], fmt['recipient_city'], fmt['payment_code'], fmt['model'], fmt['reference_number'], fmt['payment_purpose'])
    
    def assign_money_transfers(self, fmts:List[Dict[str, any]]):
        for fmt in fmts:
            self.money_transfers.append(self.assign_money_transfer(fmt))

    def assign_exchange_transaction(self, fet:Dict[str, any]):
        return ExchangeTransaction(fet['transaction_id'], fet['user_id'], fet['from_account_id'], fet['to_account_id'], fet['from_amount'], fet['to_amount'], fet['exchange_rate'], fet['fee'], fet['transaction_date'], fet['from_currency'], fet['to_currency'])
    
    def assign_exchange_transactions(self, fets:List[Dict[str, any]]):
        for fet in fets:
            self.exchange_transactions.append(self.assign_exchange_transaction(fet))

    def assign_payment(self, fp:Dict[str, any]):
        return Payment(fp['payment_id'], fp['account_id'], fp['amount_paid'], fp['paid_to'], fp['payment_date'])
    
    def assign_payments(self, fps:List[Dict[str, any]]):
        for fp in fps:
            self.payments.append(self.assign_payment(fp))

    def pay_bill(self, card:CreditCard, bill:Bill):
        etcher = Etcher()
        current_date = datetime.today().date()
        if card.expiration_date > current_date:    
            if card.status == 'active':
                if self.balance >= bill.bill_amount:
                    self.balance -= bill.bill_amount
                    etcher.updateBill(bill.bill_id)
                    etcher.uploadBillPayment(bill.bill_id, bill.account_id, bill.bill_amount, bill.biller_name)
                    etcher.updateBalance(self.account_id, self.balance)
                    message = 'Success.'
                else:
                    message = 'Insufficient funds.'
            else:
                message = 'Card inactive.'
        else:
            message = 'Card expired.'
        return message
    
    def buy_foreign_currency(self, other_account, amount_to_buy):
        if((self.currency == "RSD") and (other_account.currency != "RSD")):
            etcher = Etcher()
            rate = ExchangeRate(other_account.currency)
            amount_to_subtract, fee, rate_of_exchange = rate.rsd_to_foreign(amount_to_buy)
            self.balance -= amount_to_subtract
            self.balance -= fee
            etcher.updateBalance(self.account_id, self.balance)
            other_account.balance += amount_to_buy
            etcher.updateBalance(other_account.account_id, other_account.balance)
            etcher.uploadExchangeTransaction(self.user_id, self.account_id, other_account.account_id, amount_to_subtract, amount_to_buy, rate_of_exchange, fee, self.currency, other_account.currency)
            return 1
        else:
            return 0
        
    def sell_foreign_currency(self, other_account, amount_to_sell):
        if((self.currency != "RSD") and (other_account.currency == "RSD")):
            etcher = Etcher()
            rate = ExchangeRate(self.currency)
            amount_to_add, fee, rate_of_exchange = rate.foreign_to_rsd(amount_to_sell)
            self.balance -= amount_to_sell
            etcher.updateBalance(self.account_id, self.balance)
            other_account.balance += amount_to_add - fee
            etcher.updateBalance(other_account.account_id, other_account.balance)
            etcher.uploadExchangeTransaction(self.user_id, self.account_id, other_account.account_id, amount_to_sell, amount_to_add, rate_of_exchange, fee, self.currency, other_account.currency)
            return 'success'
        else:
            return 'Domestic currency must be bought from a foreign currency account.'

    def transfer_money(self, other_account, amount, recipient_name, recipient_address, recipient_city, payment_code, model, reference_number, payment_purpose):
        etcher = Etcher()
        self.balance -= amount
        other_account.balance += amount
        etcher.updateBalance(self.account_id, self.balance)
        etcher.updateBalance(other_account.account_id, other_account.balance)
        etcher.uploadMoneyTransfer(self.account_id, other_account.account_id, amount, recipient_name, recipient_address, recipient_city, payment_code, model, reference_number, payment_purpose)

    def create_saving(self, goal_amount, goal_name, start_date, end_date):
        etcher = Etcher()
        etcher.uploadSaving(self.user_id, self.account_id, goal_amount, goal_name, start_date, end_date, 0)

    def add_to_saving(self, saving:Saving, amount):
        etcher = Etcher()
        self.balance -= amount
        etcher.updateBalance(self.account_id, self.balance)
        saving.saved_amount += amount
        etcher.updateSaving(saving.savings_id, saving.saved_amount)

    def withdraw_from_saving(self, saving:Saving, amount):
        etcher = Etcher()
        self.balance += amount
        etcher.updateBalance(self.account_id, self.balance)
        saving.saved_amount -= amount
        etcher.updateSaving(saving.savings_id, saving.saved_amount)
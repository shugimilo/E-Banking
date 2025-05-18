from utils.database import Database

class ExchangeRate:
    def __init__(self, currency):
        db = Database()
        query = "SELECT DISTINCT r.rate_id, r.currency, r.buying_rate, r.mean_rate, r.selling_rate FROM exchange_rates r WHERE currency = %s;"
        results = db.query(query, (currency, ))
        if results:
            result = results[0]
            self.rate_id = result['rate_id']
            self.currency = result['currency']
            self.buying_rate = float(result['buying_rate'])
            self.mean_rate = float(result['mean_rate'])
            self.selling_rate = float(result['selling_rate'])

    def rsd_to_foreign(self, amount_to_buy):
        amount_to_subtract = round(amount_to_buy * self.selling_rate, 2)
        fee = round(amount_to_buy * (self.selling_rate - self.mean_rate), 2)
        return amount_to_subtract, fee, self.selling_rate
    
    def foreign_to_rsd(self, amount_to_sell):
        amount_to_add = round(amount_to_sell * self.buying_rate, 2)
        fee = round(amount_to_sell * (self.mean_rate - self.buying_rate), 2)
        return amount_to_add, fee, self.buying_rate
class Saving:
    def __init__(self, savings_id, user_id, account_id, goal_amount, goal_name, start_date, end_date, saved_amount, status):
        self.savings_id = savings_id
        self.user_id = user_id
        self.account_id = account_id
        self.goal_amount = float(goal_amount)
        self.goal_name = goal_name
        self.start_date = start_date
        self.end_date = end_date
        self.saved_amount = float(saved_amount)
        self.status = status
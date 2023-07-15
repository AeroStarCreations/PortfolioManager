class BaseInvestment:
    def __init__(self):
        self.amount_invested = 0
        self.initial_balance = 0.0
        self.target_balance = 0
        self.target_percentage = 0
        self.initial_percentage = 0.0

    def is_deficit(self):
        return self.initial_balance + self.amount_invested < self.target_balance

    def set_target_balance(self, portfolio_target_balance):
        self.target_balance = self.target_percentage / 100 * portfolio_target_balance

    def get_total_balance(self):
        return self.initial_balance + self.amount_invested

    def invest(self, investment_value):
        self.amount_invested += investment_value

    def get_percent_fill(self):
        return self.get_total_balance() / self.target_balance
    
    def get_cash_needed_to_reach_percent_fill(self, target_percent_fill):
        return (target_percent_fill * self.target_balance) - self.initial_balance - self.amount_invested

    def __str__(self):
        return 'Uh-oh! You need to override this superclass method!'

    def __repr__(self):
        return str(self)
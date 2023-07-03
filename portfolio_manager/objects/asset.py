from portfolio_manager.objects.base_investment import BaseInvestment

class Asset(BaseInvestment):
    account_id = ""
    symbol = ""
    description = ""
    quantity = 0
    last_price = 0
    last_price_change = 0
    todays_gain_cent = 0
    todays_gain_percent = 0
    total_gain_cent = 0
    total_gain_percent = 0
    cost_basis_share = 0
    cost_basis_total = 0
    category = ""

    @classmethod
    def from_symbol(cls, symbol):
        asset = cls()
        asset.symbol = symbol
        return asset

    def set_target_percentage(self, percentage):
        self.target_percentage = percentage

    def pretty_print(self):
        print((f'Account ID .......... {self.account_id}\n'
            f'Symbol .............. {self.symbol}\n'
            f'Description ......... {self.description}\n'
            f'Quantity ............ {self.quantity}\n'
            f'Last Price .......... {self.__cents_to_dollar_str(self.last_price)}\n'
            f'Last Price Change ... {self.__cents_to_dollar_str(self.last_price_change)}\n'
            f'Current Value ....... {self.__cents_to_dollar_str(self.initial_balance)}\n'
            f'Today\'s Gain Dollar . {self.__cents_to_dollar_str(self.todays_gain_cent)}\n'
            f'Today\'s Gain Percent  {self.__cents_to_dollar_str(self.todays_gain_percent)}\n'
            f'Total Gain Dollar ... {self.__cents_to_dollar_str(self.total_gain_cent)}\n'
            f'Total Gain Percent .. {self.__cents_to_dollar_str(self.total_gain_percent)}\n'
            f'Cost Basis Per Share  {self.__cents_to_dollar_str(self.cost_basis_share)}\n'
            f'Cost Basis Total .... {self.__cents_to_dollar_str(self.cost_basis_total)}\n'
            f'Type ................ {self.category}'
        ))

    def __cents_to_dollar_str(self, var):
        if var == 'n/a':
            return var
        result = f'${abs(var/100):,.2f}'
        if var < 0:
            return f'({result})'
        return result

    def __str__(self):
        return f'{self.symbol:6}: Initial: {self.__cents_to_dollar_str(self.initial_balance)}\tInvest: {self.__cents_to_dollar_str(self.amount_invested)}\tFinal: {self.__cents_to_dollar_str(self.initial_balance + self.amount_invested)})'

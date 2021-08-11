from constants import ACCOUNTS
from portfolio_manager.objects.account import Account

class Portfolio():
    accounts = {}

    def __init__(self, parsed_assets):
        for key, account_details in ACCOUNTS.items():
            self.accounts[account_details.id] = Account(parsed_assets, account_details)

    def invest_balanced(self, account_details, additional_cash = 0):
        return self.accounts[account_details.id].invest_balanced(additional_cash)

    def print_categories(self, account_details):
        self.accounts[account_details.id].pretty_print_categories()

    def print_assets(self, account_details):
        self.accounts[account_details.id].pretty_print_assets()

from portfolio_manager.objects.account import Account
from portfolio_manager.objects.asset import Asset

class Portfolio():

    def __init__(self, parsed_assets, account_details_list):
        assert isinstance(parsed_assets, list), 'Portfolio requires @parsed_assets be a list'
        assert isinstance(account_details_list, list), 'Portfolio requires @account_details_list be a list'
        assert all([isinstance(asset, Asset) for asset in parsed_assets]), '@parsed_assets must contain items of type Asset'
        
        self.accounts = {}
        for account_details in account_details_list:
            self.accounts[account_details.id] = Account(parsed_assets, account_details)

    def invest_balanced(self, account_details, additional_cash = 0):
        return self.accounts[account_details.id].invest_balanced(additional_cash)

    def get_assets(self, account_details):
        return self.accounts[account_details.id].get_assets()

    def print_categories(self, account_details):
        self.accounts[account_details.id].pretty_print_categories()

    def print_assets(self, account_details):
        self.accounts[account_details.id].pretty_print_assets()

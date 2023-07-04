from objects.account import Account
from objects.account_details import AccountDetails
from objects.asset import Asset

class Portfolio():

    def __init__(self, parsed_assets: list[Asset], account_details_list: list[AccountDetails]):
        assert isinstance(parsed_assets, list), 'Portfolio requires @parsed_assets be a list'
        assert isinstance(account_details_list, list), 'Portfolio requires @account_details_list be a list'
        assert all([isinstance(asset, Asset) for asset in parsed_assets]), '@parsed_assets must contain items of type Asset'
        assert all([isinstance(ad, AccountDetails) for ad in account_details_list]), '@account_details_list must contain items of type AccountDetails'
        
        self.accounts: dict[Account] = {}
        for account_details in account_details_list:
            self.accounts[account_details.id] = Account(parsed_assets, account_details)

    def invest_balanced(self, account_id, additional_cash = 0):
        return self.accounts[account_id].invest_balanced(additional_cash)

    def get_assets(self, account_id):
        return self.accounts[account_id].get_assets()

    def print_categories(self, account_id):
        self.accounts[account_id].pretty_print_categories()

    def print_assets(self, account_id):
        self.accounts[account_id].pretty_print_assets()

from .account import Account
from .account_details import AccountDetails
from .asset import Asset

class Portfolio():

    def __init__(self, parsed_assets: list[Asset], account_details_list: list[AccountDetails]):
        """
        Portfolio constructor

        Args:
            parsed_assets (list[Asset]): List of Assets that represent current account holdings.
            account_details_list (list[AccountDetails]): List of AccountDetails that represent desired account holdings.
        """
        assert isinstance(parsed_assets, list), 'Portfolio requires @parsed_assets be a list'
        assert isinstance(account_details_list, list), 'Portfolio requires @account_details_list be a list'
        assert all([isinstance(asset, Asset) for asset in parsed_assets]), '@parsed_assets must contain items of type Asset'
        assert all([isinstance(ad, AccountDetails) for ad in account_details_list]), '@account_details_list must contain items of type AccountDetails'
        
        self.accounts: dict[str, Account] = {}
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

    def print_assets_summary(self, account_id):
        self.accounts[account_id].pretty_print_assets_summary()

    def get_cash_balance(self, account_id) -> float:
        return self.accounts[account_id].get_cash_balance()

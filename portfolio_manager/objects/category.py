from .asset import Asset
from ..utils import format_dollars
from .base_investment import BaseInvestment
from .balanceable import Balanceable
from .. import balancer

class Category(BaseInvestment, Balanceable):

    def __init__(self, name, assets: list[Asset]):
        super().__init__()
        self.name = name
        self.assets = assets
        self.target_percentage = self.__get_target_percentage(assets)
        self.initial_balance = self.__get_initial_value(assets)
        
    def invest(self, investment_value):
        super().invest(investment_value)
        balancer.balanced_invest(self, investment_value)
    
    def set_target_balance(self, account_target_balance):
        super().set_target_balance(account_target_balance)
        for asset in self.assets:
            asset.set_target_balance(account_target_balance)
    
    def get_deficit_items(self):
        return [asset for asset in self.assets if asset.is_deficit()]

    def __get_target_percentage(self, assets):
        return sum([asset.target_percentage for asset in self.assets])

    def __get_initial_value(self, assets):
        return sum([asset.initial_balance for asset in assets])

    def __str__(self):
        return f'{self.name:15}: Initial: {format_dollars(self.initial_balance)}\tInvest: {format_dollars(self.amount_invested)}\tFinal: {format_dollars(self.initial_balance + self.amount_invested)}'
        # return f'{self.name:15}: Initial: {self.__cents_to_dollar_str(self.initial_balance)}\tInvest: {self.__cents_to_dollar_str(self.amount_invested)}\tFinal: {self.__cents_to_dollar_str(self.initial_balance + self.amount_invested)})'

from .objects.account_details import AccountDetails
from .objects.allocation_category import AllocationCategory
from .objects.allocation import Allocation
from .objects.asset import Asset
from .objects.portfolio import Portfolio

def bob():
    print('Hello, World!!')
    
def start():
    from main import main
    main()
    
def start_kraken(portfolio: Portfolio):
    from main import manage_kraken
    manage_kraken(portfolio)
    
# def invest_balanced_binance(account_balances):
#     main.investBalancedBinance(account_balances)
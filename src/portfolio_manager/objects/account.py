from portfolio_manager.objects.category import Category
from portfolio_manager.objects.balanceable import Balanceable
from portfolio_manager.objects.asset import Asset
import constants
from constants import format_cents
import balancer

class Account(Balanceable):
    __CASH = 'FCASH'

    def __init__(self, parsed_assets, account_details):
        self.__categories = []
        self.__initial_balance = 0
        self.__target_balance = 0
        self.__cash_balance = 0

        # Get asset allocation targets for this account
        allocations = {}
        if account_details.name == 'Index Fund':
            allocations = constants.INDEX_FUND_ALLOCATIONS
        elif account_details.name == 'ETF':
            allocations = constants.ETF_ALLOCATIONS
        elif account_details.name == 'Junkyard':
            allocations = constants.JUNKYARD_ALLOCATIONS

        # Get category info for this account
        for _id, info in allocations.items():
            category_assets = []
            for symbol, percentage in info['assets'].items():
                parsed_asset = None
                try:
                    # Try to get the asset/symbol from the parsed CSV file results.
                    parsed_asset = [asset for asset in parsed_assets if asset.symbol == symbol][0]
                except:
                    # If the asset does not exist in parsed_assets then it's a new addition. Create empty Asset object.
                    parsed_asset = Asset.from_symbol(symbol)
                
                self.__initial_balance += parsed_asset.initial_balance
                parsed_asset.set_target_percentage(percentage)
                category_assets.append(parsed_asset)

            self.__categories.append(Category(_id, info['name'], category_assets))
        
        # Get the initial cash balance
        try:
            self.__cash_balance = [asset.initial_balance for asset in parsed_assets if asset.symbol == self.__CASH and asset.account_id == account_details.id][0]
        except:
            pass

    def invest_balanced(self, additional_cash = 0):
        self.__target_balance = self.__initial_balance + self.__cash_balance + additional_cash
        for category in self.__categories:
            category.set_target_balance(self.__target_balance)
        return balancer.balanced_invest(self, additional_cash + self.__cash_balance)

    def get_initial_balance(self):
        return self.__initial_balance

    def get_deficit_items(self):
        return [category for category in self.__categories if category.is_deficit()]

    def pretty_print_categories(self):
        titles = ['Names', 'Target %', 'Target $', 'Current %', 'Current $', 'Final %', 'Final $']
        num_columns = len(titles)
        columns = [[] for x in titles]
        column_widths = []

        # Get the data
        for c in self.__categories:
            columns[0].append(c.name)
            columns[1].append(f'{c.target_percentage*100:.1f}%')
            columns[2].append(format_cents(c.target_balance))
            try:
                columns[3].append(f'{c.initial_balance/self.__initial_balance*100:.1f}%')
            except ZeroDivisionError:
                columns[3].append('n/a')
            columns[4].append(format_cents(c.initial_balance))
            columns[5].append(f'{c.get_total_balance()/self.__target_balance*100:.1f}%')
            columns[6].append(format_cents(c.get_total_balance()))

        # Get column widths
        for i in range(len(titles)):
            column_widths.append(self.__longest_member(titles[i], columns[i]))
        
        header = ''
        for i in range(len(titles)):
            header += f'| {titles[i]:{column_widths[i]}} '
        header += '|'

        table_width = len(header)
        divider_line = ''
        for i in range(table_width):
            divider_line += '-'

        print('\nCATEGORIES')
        print(divider_line)
        print(header)
        print(divider_line)

        # Print each data row
        num_rows = len(columns[0])
        for i in range(num_rows):
            line = ''
            for j in range(num_columns):
                line += f'| {columns[j][i]:>{column_widths[j]}} '
            print(line + '|')

        print(divider_line)

    def pretty_print_assets(self):
        titles = ['Symbol', 'Buy', 'Target %', 'Target $', 'Current %', 'Current $', 'Final %', 'Final $']
        num_columns = len(titles)
        columns = [[] for x in titles]
        column_widths = []

        # Get the data
        for c in self.__categories:
            for a in c.assets:
                columns[0].append(a.symbol)
                columns[1].append(format_cents(a.amount_invested))
                columns[2].append(f'{a.target_percentage*100:.1f}%')
                columns[3].append(format_cents(a.target_balance))
                try:
                    columns[4].append(f'{a.initial_balance/self.__initial_balance*100:.1f}%')
                except ZeroDivisionError:
                    columns[4].append('n/a')
                columns[5].append(format_cents(a.initial_balance))
                columns[6].append(f'{a.get_total_balance()/self.__target_balance*100:.1f}%')
                columns[7].append(format_cents(a.get_total_balance()))

        # Get column widths
        for i in range(len(titles)):
            column_widths.append(self.__longest_member(titles[i], columns[i]))

        # Get header row
        header = ''
        for i in range(len(titles)):
            header += f'| {titles[i]:{column_widths[i]}} '
        header += '|'

        table_width = len(header)
        divider_line = ''
        for i in range(table_width):
            divider_line += '-'

        print('\nASSETS')
        print(divider_line)
        print(header)
        print(divider_line)

        # Print each data row
        num_rows = len(columns[0])
        for i in range(num_rows):
            line = ''
            for j in range(num_columns):
                line += f'| {columns[j][i]:>{column_widths[j]}} '
            print(line + '|')

        print(divider_line)

    def __longest_member(self, title, str_list):
        return max([len(x) for x in str_list + [title]])

    def __str__(self):
        return f'Portfolio | {format_cents(self.__initial_balance)}'

    def __repr__(self):
        return str(self)
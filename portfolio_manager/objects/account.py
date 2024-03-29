from itertools import chain
from ..utils import format_cents, format_dollars
from .category import Category
from .balanceable import Balanceable
from .asset import Asset
from ..constants import CASH_SYMBOLS, BOLD, END
from .. import balancer
from .account_details import AccountDetails

class Account(Balanceable):

    def __init__(self, parsed_assets: list[Asset], account_details: AccountDetails):
        self.__categories: list[Category] = []
        self.__initial_balance = 0
        self.__target_balance = 0
        # self.__cash_balance = 0
        self.__account_details = account_details
        self.__cash_asset = None

        # Get category info for this account
        for allocation_category in account_details.asset_allocation.get_categories():
            category_assets = []
            for symbol, percentage in allocation_category.get_assets().items():
                parsed_asset = None
                try:
                    # Try to get the asset/symbol from @parsed_assets
                    parsed_asset = next(asset for asset in parsed_assets if asset.symbol == symbol)
                except StopIteration:
                    print(f'ERROR: Could not find {symbol} in parsed assets. Will create blank Asset.')
                    parsed_asset = Asset.from_symbol(symbol)

                self.__initial_balance += parsed_asset.initial_balance
                parsed_asset.set_target_percentage(percentage)
                category_assets.append(parsed_asset)

                # Snag the cash asset
                if symbol in CASH_SYMBOLS:
                    self.__cash_asset = parsed_asset

            self.__categories.append(Category(allocation_category.name, category_assets))
        
        # Set initial allocation for each asset
        for c in self.__categories:
            for a in c.assets:
                a.initial_percentage = a.initial_balance / self.__initial_balance

        # Get the initial cash balance
        # try:
        #     self.__cash_balance = [asset.initial_balance for asset in parsed_assets if asset.symbol in CASH_SYMBOLS and asset.account_id == account_details.id][0]
        # except:
        #     pass

    def invest_balanced(self, additional_cash = 0):
        self.__target_balance = self.__initial_balance + additional_cash
        for category in self.__categories:
            category.set_target_balance(self.__target_balance)
        amount_invested = balancer.balanced_invest(self, additional_cash + self.__cash_asset.initial_balance)
        self.__cash_asset.invest(-amount_invested)
        return amount_invested

    def get_assets(self) -> list[Asset]:
        return list(chain.from_iterable([category.assets for category in self.__categories]))

    def get_initial_balance(self):
        return self.__initial_balance

    def get_deficit_items(self) -> list[Category]:
        return [category for category in self.__categories if category.is_deficit()]

    def get_name(self):
        return self.__account_details.name
    
    def get_id(self):
        return self.__account_details.id

    def get_cash_balance(self):
        return self.__cash_asset.initial_balance
    
    def __make_bold(self, strings):
        new_strings = []
        for string in strings:
            new_strings.append(f'{BOLD}{string}{END}')
        return new_strings

    def pretty_print_categories(self):
        titles = ['Names', 'Target %', 'Target $', 'Current %', 'Current $', 'Final %', 'Final $']
        num_columns = len(titles)
        columns = [[] for x in titles]
        column_widths = []

        # Get the data
        for c in self.__categories:
            columns[0].append(c.name)
            columns[1].append(f'{c.target_percentage:.1f}%')
            # columns[2].append(format_cents(c.target_balance))
            columns[2].append(format_dollars(c.target_balance))
            try:
                columns[3].append(f'{100*(c.initial_balance/self.__initial_balance):.1f}%')
            except ZeroDivisionError:
                columns[3].append('n/a')
            # columns[4].append(format_cents(c.initial_balance))
            columns[4].append(format_dollars(c.initial_balance))
            try:
                columns[5].append(f'{100*(c.get_total_balance()/self.__target_balance):.1f}%')
            except ZeroDivisionError:
                columns[5].append('0%')
            # columns[6].append(format_cents(c.get_total_balance()))
            columns[6].append(format_dollars(c.get_total_balance()))

        # Get column widths
        for i in range(len(titles)):
            column_widths.append(self.__longest_member(titles[i], columns[i]))
        
        header = ''
        for i in range(len(titles)):
            header += f'| {BOLD}{titles[i]:{column_widths[i]}}{END} '
        header += '|'

        table_width = len(header) - len(titles) * (len(BOLD) + len(END))
        divider_line = ''
        for i in range(table_width):
            divider_line += '-'

        print(f'\n{BOLD}CATEGORIES{END}')
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
                # columns[1].append(format_cents(a.amount_invested))
                columns[1].append(format_dollars(a.amount_invested))
                columns[2].append(f'{a.target_percentage:.1f}%')
                # columns[3].append(format_cents(a.target_balance))
                columns[3].append(format_dollars(a.target_balance))
                try:
                    columns[4].append(f'{100*(a.initial_balance/self.__initial_balance):.1f}%')
                except ZeroDivisionError:
                    columns[4].append('n/a')
                # columns[5].append(format_cents(a.initial_balance))
                columns[5].append(format_dollars(a.initial_balance))
                try:
                    columns[6].append(f'{100*(a.get_total_balance()/self.__target_balance):.1f}%')
                except ZeroDivisionError:
                    columns[6].append('0%')
                # columns[7].append(format_cents(a.get_total_balance()))
                columns[7].append(format_dollars(a.get_total_balance()))

        # Get column widths
        for i in range(len(titles)):
            column_widths.append(self.__longest_member(titles[i], columns[i]))

        # Get header row
        header = ''
        for i in range(len(titles)):
            header += f'| {BOLD}{titles[i]:{column_widths[i]}}{END} '
        header += '|'

        table_width = len(header) - len(titles) * (len(BOLD) + len(END))
        divider_line = ''
        for i in range(table_width):
            divider_line += '-'

        print(f'\n{BOLD}ASSETS{END}')
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

    def pretty_print_assets_summary(self):
        titles = ['Symbol', 'Quantity', 'Value ($)', 'Slice (%)']
        num_columns = len(titles)
        columns = [[] for t in titles]
        column_widths = []
        total_value = 0.0

        # Get the data
        for c in self.__categories:
            for a in c.assets:
                total_value += a.initial_balance
                columns[0].append(a.symbol)
                columns[1].append(str(a.quantity).rstrip('0'))
                columns[2].append(f'{a.initial_balance:,.4f}')
                columns[3].append(f'{a.initial_percentage*100:.2f}')

        # Get column widths
        for i in range(len(titles)):
            column_widths.append(self.__longest_member(titles[i], columns[i]))

        # Get header row
        header = ''
        for i in range(len(titles)):
            header += f'| {BOLD}{titles[i]:^{column_widths[i]}}{END} '
        header += '|'

        table_width = len(header) - len(titles) * (len(BOLD) + len(END))
        divider_line = ''
        for i in range(table_width):
            divider_line += '-'

        print(f'\n{BOLD}Portfolio Value: ${total_value:,.2f}{END}\n')
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

    def __longest_member(self, title: str, str_list: list[str]):
        return max([len(x) for x in str_list + [title]])

    def __str__(self):
        # return f'Portfolio | {format_cents(self.__initial_balance)}'
        return f'Portfolio | {format_dollars(self.__initial_balance)}'

    def __repr__(self):
        return str(self)